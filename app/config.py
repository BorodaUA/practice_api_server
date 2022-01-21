import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration variables for the project."""

    SECRET_KEY = os.getenv(key='SECRET_KEY', default='very secret key')
    APP_HOST = os.getenv(key='APP_HOST', default='0.0.0.0')
    APP_PORT = os.getenv(key='APP_PORT', default=4800)


class DevelopmentConfig(BaseConfig):
    """Development configuration variables for the project."""

    CONFIG_NAME = "development"
    ENV = "development"
    DEBUG = True
    TESTING = False


configs = {
    'development': DevelopmentConfig,
}
