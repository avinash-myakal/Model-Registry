from flask import Flask
from flask_cors import CORS

from flask_dotenv import DotEnv
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from werkzeug.middleware.proxy_fix import ProxyFix

from tno.mmvib_registry.settings import EnvSettings

api = Api()
env = DotEnv()
sa = SQLAlchemy()


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. influxdbgraphs.api.settings.ProdConfig
    """
    from tno.shared.log import get_logger

    logger = get_logger(__name__)
    logger.info("Setting up app.")

    app = Flask(__name__)
    app.config.from_object(object_name)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    env.init_app(app, env_file=".env")
    api.init_app(app)

    # Register blueprints.
    from tno.mmvib_registry.apis.status import api as status_api
    from tno.mmvib_registry.apis.registry import api as registry_api

    api.register_blueprint(status_api)
    api.register_blueprint(registry_api)

    CORS(app, resources={r"/*": {"origins": "*"}})

    if EnvSettings.db_type() == "postgres":
        sa.init_app(app)
        engine = create_engine(EnvSettings.sqlalchemy_database_uri())
        if not database_exists(engine.url):
            create_database(engine.url)
        with app.app_context():
            sa.create_all()
    logger.info("Finished setting up app.")

    return app
