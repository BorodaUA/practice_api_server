from flask import Config

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy_utils import create_database, database_exists, drop_database

from app import create_app
from app.config import TestingConfig
from auth.services import AuthService
from common.constants.auth import AuthJWTConstants
from common.tests.test_data.users import request_test_user_data
from db import Base, get_session
from users.models import User
from users.services import UserService


class TestMixin:
    """Generic test helper class."""

    def setUp(self) -> None:
        self.app = create_app(config_name=TestingConfig.CONFIG_NAME)
        self.context = self.app.test_request_context()
        self.context.push()
        # Database creation.
        self.db_url = self.create_db_url(config=self.app.config)
        self.create_db(url=self.db_url)
        # Tables creation.
        self.create_tables(engine=self.app.db_engine, Base=Base)
        # Test db session creation.
        self.db_session = get_session(engine=self.app.db_engine)
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        self.context.pop()
        self.db_session.remove()
        self.drop_db(url=self.db_url)

    def create_db(self, url: str) -> None:
        """Create test database in postgres server."""
        if database_exists(url):
            drop_database(url)
        create_database(url)

    def drop_db(self, url) -> None:
        """Delete test database from postgres server."""
        if database_exists(url):
            drop_database(url)

    def create_db_url(self, config: Config) -> str:
        """Return formatted postgres db url."""
        return (
            f'{config["POSTGRES_DIALECT_DRIVER"]}://{config["POSTGRES_DB_USERNAME"]}:'
            f'{config["POSTGRES_DB_PASSWORD"]}@{config["POSTGRES_DB_HOST"]}:'
            f'{config["POSTGRES_DB_PORT"]}/{config["POSTGRES_DB_NAME"]}'
        )

    def create_tables(self, engine: Engine, Base: DeclarativeMeta) -> None:
        """Create db tables in test database."""
        Base.metadata.create_all(engine)

    def add_user_to_db(self) -> User:
        """Create test user data in test db."""
        return UserService(session=self.db_session)._save_user_data(user=request_test_user_data.ADD_USER_TEST_DATA)

    def authorize_user(self):
        """Add authorization cookies to the test client."""
        user = self.add_user_to_db()
        auth_service = AuthService(session=self.db_session)
        access_token = auth_service._create_jwt_token(
            identity=user.id,
            token_type=AuthJWTConstants.ACCESS_TOKEN_NAME.value,
            time_amount=AuthJWTConstants.TOKEN_EXPIRE_60.value,
            time_unit=AuthJWTConstants.MINUTES.value,
        )
        refresh_token = auth_service._create_jwt_token(
            identity=user.id,
            token_type=AuthJWTConstants.REFRESH_TOKEN_NAME.value,
            time_amount=AuthJWTConstants.TOKEN_EXPIRE_7.value,
            time_unit=AuthJWTConstants.DAYS.value,
        )
        self.client.set_cookie(
            server_name=self.app.config['SERVER_NAME'],
            key=AuthJWTConstants.JWT_ACCESS_COOKIE_NAME.value,
            value=access_token,
        )
        self.client.set_cookie(
            server_name=self.app.config['SERVER_NAME'],
            key=AuthJWTConstants.JWT_REFRESH_COOKIE_NAME.value,
            value=refresh_token,
        )
