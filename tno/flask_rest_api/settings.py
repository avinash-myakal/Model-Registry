import os
import secrets

from dotenv import load_dotenv

load_dotenv(verbose=True)

DATA_FOLDER = os.path.join(os.path.abspath(os.getcwd()), "backend", "data")


class EnvSettings:
    @staticmethod
    def env() -> str:
        return os.getenv("ENV", "dev")

    @staticmethod
    def flask_server_host() -> str:
        return "0.0.0.0"

    @staticmethod
    def flask_server_port() -> int:
        return 9200

    @staticmethod
    def is_production():
        return EnvSettings.env() == "prod"

    @staticmethod
    def postgres_host() -> str:
        return os.getenv("POSTGRES_HOST", "localhost")

    @staticmethod
    def postgres_port() -> str:
        return os.getenv("POSTGRES_PORT", "9232")

    @staticmethod
    def postgres_user() -> str:
        return os.getenv("POSTGRES_USER", "flask_rest_api")

    @staticmethod
    def postgres_password() -> str:
        return os.getenv("POSTGRES_PASSWORD", "flask_rest_api")

    @staticmethod
    def postgres_db() -> str:
        return os.getenv("POSTGRES_DB", "flask_rest_api")

    @staticmethod
    def influxdb_host() -> str:
        return os.getenv("INFLUXDB_HOST", "influxdb")

    @staticmethod
    def influxdb_port() -> int:
        return int(os.getenv("INFLUXDB_PORT", "9286"))

    @staticmethod
    def influxdb_user() -> str:
        return os.getenv("INFLUXDB_USER", "flask_rest_api")

    @staticmethod
    def influxdb_password() -> str:
        return os.getenv("INFLUXDB_USER_PASSWORD", "flask_rest_api")


class Config(object):
    """Generic config for all environments."""

    SECRET_KEY = secrets.token_urlsafe(16)

    API_TITLE = "TNO Flask REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )

    API_SPEC_OPTIONS = {
        "info": {
            "description": "This is the TNO flask_rest_api backend API.",
            "termsOfService": "https://www.tno.nl",
            "contact": {"email": "test@swagger.io"},
            "license": {"name": "TBD", "url": "https://www.tno.nl"},
        }
    }

    # JWT_TOKEN_LOCATION = 'headers'
    # JWT_HEADER_NAME = 'Authorization'
    # JWT_HEADER_TYPE = 'Bearer'
    # JWT_SECRET_KEY = 'super-secret'  # Change this!
    # JWT_ACCESS_TOKEN_EXPIRES = 3600
    # JWT_ERROR_MESSAGE_KEY = 'message'

    POSTGRES_HOST = EnvSettings.postgres_host()
    POSTGRES_PORT = EnvSettings.postgres_port()
    POSTGRES_USER = EnvSettings.postgres_user()
    POSTGRES_PASSWORD = EnvSettings.postgres_password()
    POSTGRES_DB = EnvSettings.postgres_db()
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    ENV = "prod"
    DEBUG = False
    FLASK_DEBUG = False


class DevConfig(Config):
    ENV = "dev"
    DEBUG = True
    FLASK_DEBUG = True
