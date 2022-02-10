from sqlalchemy_utils import create_database, database_exists
from tno.flask_rest_api import db
from tno.flask_rest_api.main import app
from tno.shared.log import get_logger

logger = get_logger("tno.flask_rest_api.main")


@app.cli.command("createdb")
def createdb_command():
    """Destroys and creates the database + tables."""

    # Need to import models to create tables.
    import tno.flask_rest_api.dbmodels  # noqa

    db_url = app.config["SQLALCHEMY_DATABASE_URI"]
    try:
        if not database_exists(db_url):
            print("Creating database.")
            create_database(db_url)
    except Exception:
        pass

    print("Creating tables.")
    db.create_all()
    db.session.commit()
    print("Shiny!")


