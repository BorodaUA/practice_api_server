import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration variables for the project."""

    SECRET_KEY = os.getenv(key='SECRET_KEY', default='very secret key')
    APP_HOST = os.getenv(key='APP_HOST', default='0.0.0.0')
    APP_PORT = os.getenv(key='APP_PORT', default=4800)
    POSTGRES_DIALECT_DRIVER = os.getenv(key='POSTGRES_DIALECT_DRIVER', default='postgresql+psycopg2')
    POSTGRES_DB_USERNAME = os.getenv(key='POSTGRES_DB_USERNAME', default='postgres')
    POSTGRES_DB_PASSWORD = os.getenv(key='POSTGRES_DB_PASSWORD', default='postgres')
    POSTGRES_DB_HOST = os.getenv(key='POSTGRES_DB_HOST', default='postgres_server')
    POSTGRES_DB_PORT = os.getenv(key='POSTGRES_DB_PORT', default=5432)
    POSTGRES_DB_NAME = os.getenv(key='POSTGRES_DB_NAME', default='postgres')
    POSTGRES_DB_URL = (
        f'{POSTGRES_DIALECT_DRIVER}://{POSTGRES_DB_USERNAME}:{POSTGRES_DB_PASSWORD}@'
        f'{POSTGRES_DB_HOST}:{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}'
    )


class DevelopmentConfig(BaseConfig):
    """Development configuration variables for the project."""

    CONFIG_NAME = "development"
    ENV = "development"
    DEBUG = True
    TESTING = False


configs = {
    'development': DevelopmentConfig,
}
