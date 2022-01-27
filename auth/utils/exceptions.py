from flask import Response, jsonify, make_response

from common.constants.http import HttpStatusCodeConstants


class AuthUserInvalidPasswordException(Exception):
    pass


def invalid_user_password_error_handler(error: AuthUserInvalidPasswordException) -> Response:
    """Custom AuthUserInvalidPasswordException handler return http Response with error message."""
    return make_response(jsonify({'message': str(error)}), HttpStatusCodeConstants.HTTP_401_UNAUTHORIZED.value)
