import os
import secrets

from dotenv import load_dotenv

load_dotenv(verbose=True)


class EnvSettings:
    @staticmethod
    def env() -> str:
        return os.getenv("ENV", "dev")

    @staticmethod
    def flask_server_host() -> str:
        return "0.0.0.0"

    @staticmethod
    def flask_server_port() -> int:
        return 9900

    @staticmethod
    def is_production():
        return EnvSettings.env() == "prod"

    @staticmethod
    def mongo_host() -> str:
        return os.getenv("MONGO_HOST", "localhost")

    @staticmethod
    def mongo_port() -> str:
        return os.getenv("MONGO_PORT", "9232")

    @staticmethod
    def mongo_user() -> str:
        return os.getenv("MONGO_USER", "flask_rest_api")

    @staticmethod
    def mongo_password() -> str:
        return os.getenv("MONGO_PASSWORD", "flask_rest_api")

    @staticmethod
    def mongo_db() -> str:
        return os.getenv("MONGO_DB", "flask_rest_api")


class Config(object):
    """Generic config for all environments."""

    SECRET_KEY = secrets.token_urlsafe(16)

    API_TITLE = "MMviB Registry REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/openapi"
    OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )

    API_SPEC_OPTIONS = {
        "info": {
            "description": "This is the MMvIB Model adapter registry API.",
            "termsOfService": "https://www.tno.nl",
            "contact": {"email": "ewoud.werkman@tno.nl"},
            "license": {"name": "TBD", "url": "https://www.tno.nl"},
        }
    }

    # JWT_TOKEN_LOCATION = 'headers'
    # JWT_HEADER_NAME = 'Authorization'
    # JWT_HEADER_TYPE = 'Bearer'
    # JWT_SECRET_KEY = 'super-secret'  # Change this!
    # JWT_ACCESS_TOKEN_EXPIRES = 3600
    # JWT_ERROR_MESSAGE_KEY = 'message'

    MONGO_HOST = EnvSettings.mongo_host()
    MONGO_PORT = EnvSettings.mongo_port()
    MONGO_USER = EnvSettings.mongo_user()
    MONGO_PASSWORD = EnvSettings.mongo_password()
    MONGO_DB = EnvSettings.mongo_db()
    #SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    ENV = "prod"
    DEBUG = False
    FLASK_DEBUG = False


class DevConfig(Config):
    ENV = "dev"
    DEBUG = True
    FLASK_DEBUG = True
