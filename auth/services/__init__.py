from datetime import timedelta
from typing import Type
import abc

from flask import Response, jsonify

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_access_cookies,
    unset_refresh_cookies,
)
from sqlalchemy.orm import scoped_session

from auth.schemas import AuthBaseSchema
from auth.services.serializers import AuthSerializer
from auth.utils.exceptions import AuthUserInvalidPasswordException
from common.constants.auth import AuthJWTConstants
from users.services import UserService
from utils.logging import setup_logging


class AbstractAuthService(metaclass=abc.ABCMeta):

    def __init__(
        self, session: scoped_session,
        input_schema: Type[AuthBaseSchema] | None = None,
        output_schema: Type[AuthBaseSchema] | None = None,
            ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.user_service = UserService(session=session)
        self.validator = AuthSerializer(input_schema, output_schema)

    def login(self, user: dict) -> Response:
        """Login user with provided credentials."""
        return self._login(user)

    def me(self) -> dict:
        """Return currently authenticated user."""
        return self._me()

    def logout(self) -> Response:
        """Logout currently authenticated user."""
        return self._logout()

    @abc.abstractclassmethod
    def _login(self, user: dict) -> None:
        pass

    @abc.abstractclassmethod
    def _me(self) -> None:
        pass

    @abc.abstractclassmethod
    def _logout(self) -> None:
        pass


class AuthService(AbstractAuthService):

    def _login(self, user: dict) -> Response:
        user = self.validator.deserialize(data=user)
        db_user = self.user_service._get_user_by_username(username=user['username'])
        if self.user_service._verify_password(user['password'], db_user.password):
            access_token = self._create_jwt_token(
                identity=db_user.id,
                token_type=AuthJWTConstants.ACCESS_TOKEN_NAME.value,
                time_amount=AuthJWTConstants.TOKEN_EXPIRE_60.value,
                time_unit=AuthJWTConstants.MINUTES.value,
            )
            refresh_token = self._create_jwt_token(
                identity=db_user.id,
                token_type=AuthJWTConstants.REFRESH_TOKEN_NAME.value,
                time_amount=AuthJWTConstants.TOKEN_EXPIRE_7.value,
                time_unit=AuthJWTConstants.DAYS.value,
            )
            response_tokens = {'access_token': access_token, 'refresh_token': refresh_token}
            self.validator.serialize(data=response_tokens)
            response = jsonify(response_tokens)

            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            self._log.debug(f'User with username: {db_user.username} logged in.')
            return response
        raise AuthUserInvalidPasswordException('Incorrect username or password.')

    def _create_jwt_token(self, identity: str, token_type: str, time_amount: int, time_unit: str) -> str:
        """Return access or refresh token with set parameters."""
        CREATE_TOKEN_METHODS = {
            'access': create_access_token,
            'refresh': create_refresh_token,
        }
        expires_delta = timedelta(**{time_unit: time_amount})
        return CREATE_TOKEN_METHODS[token_type](identity=identity, expires_delta=expires_delta)

    def _me(self) -> dict:
        user_id = get_jwt_identity()
        db_user = self.user_service._get_user(column='id', value=user_id)
        self._log.debug(f'User with username: {db_user.username} currently logged in.')
        return self.validator.serialize(data=db_user)

    def _logout(self) -> Response:
        user_id = get_jwt_identity()
        response_message = {'message': 'User successfully logged out.'}
        self.validator.serialize(data=response_message)
        response = jsonify(response_message)
        unset_access_cookies(response=response)
        unset_refresh_cookies(response=response)
        self._log.debug(f'User with id: {user_id} successfully logged out.')
        return response
