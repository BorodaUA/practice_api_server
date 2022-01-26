from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config import BaseConfig

Base = declarative_base()

engine = create_engine(url=BaseConfig.POSTGRES_DB_URL, echo=True)


def get_session() -> scoped_session:
    """Return scoped sqlalchemy session."""
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
