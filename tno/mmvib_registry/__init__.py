from flask import Blueprint, Flask
from flask_cors import CORS

from flask_dotenv import DotEnv
from flask_smorest import Api, Blueprint

from werkzeug.middleware.proxy_fix import ProxyFix

api = Api()
env = DotEnv()


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

    env.init_app(app, env_file="../../.env")
    api.init_app(app)

    # Register blueprints.
    from tno.mmvib_registry.apis.status import api as status_api
    from tno.mmvib_registry.apis.registry import api as registry_api

    api.register_blueprint(status_api)
    api.register_blueprint(registry_api)

    CORS(app, resources={r"/*": {"origins": "*"}})

    logger.info("Finished setting up app.")

    return app
