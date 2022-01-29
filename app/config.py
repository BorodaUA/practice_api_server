import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration variables for the project."""

    SECRET_KEY = os.getenv(key='SECRET_KEY', default='very secret key')
    APP_HOST = os.getenv(key='APP_HOST', default='0.0.0.0')
    APP_PORT = os.getenv(key='APP_PORT', default=4800)
    # DB configuration variables.
    POSTGRES_DIALECT_DRIVER = os.getenv(key='POSTGRES_DIALECT_DRIVER', default='postgresql+psycopg2')
    POSTGRES_DB_USERNAME = os.getenv(key='POSTGRES_DB_USERNAME', default='postgres')
    POSTGRES_DB_PASSWORD = os.getenv(key='POSTGRES_DB_PASSWORD', default='postgres')
    POSTGRES_DB_HOST = os.getenv(key='POSTGRES_DB_HOST', default='postgres_server')
    POSTGRES_DB_PORT = os.getenv(key='POSTGRES_DB_PORT', default=5432)
    POSTGRES_DB_NAME = os.getenv(key='POSTGRES_DB_NAME', default='postgres')
    # JWT configuration variables.
    JWT_SECRET_KEY = os.getenv(key='JWT_SECRET_KEY', default='jwt secret key')
    JWT_TOKEN_LOCATION = os.getenv(key='JWT_TOKEN_LOCATION', default='cookies')
    JWT_COOKIE_CSRF_PROTECT = (os.getenv(key='JWT_COOKIE_CSRF_PROTECT', default=True) == 'True')
    # sqlalchemy configuration variables.
    SQLALCHEMY_ENGINE_ECHO = (os.getenv(key='SQLALCHEMY_ENGINE_ECHO', default=False) == 'True')


class DevelopmentConfig(BaseConfig):
    """Development configuration variables for the project."""

    CONFIG_NAME = "development"
    ENV = "development"
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """Testing configuration variables for the project."""
    CONFIG_NAME = "testing"
    ENV = "testing"
    DEBUG = False
    TESTING = True
    POSTGRES_DB_NAME = 'test_postgres'


configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
