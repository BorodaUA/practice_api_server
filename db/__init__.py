from flask import Config

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


def create_db_engine(config: Config, echo: bool) -> Engine:
    """Return sqlalchemy engine instance."""
    POSTGRES_DB_URL = (
        f'{config["POSTGRES_DIALECT_DRIVER"]}://{config["POSTGRES_DB_USERNAME"]}:'
        f'{config["POSTGRES_DB_PASSWORD"]}@{config["POSTGRES_DB_HOST"]}:'
        f'{config["POSTGRES_DB_PORT"]}/{config["POSTGRES_DB_NAME"]}'
    )
    return create_engine(url=POSTGRES_DB_URL, echo=echo)


def get_session(engine: Engine) -> scoped_session:
    """Return scoped sqlalchemy session."""
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
