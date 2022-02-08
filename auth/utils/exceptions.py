from flask import Response, jsonify, make_response

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema


class AuthUserInvalidPasswordException(Exception):
    pass


def invalid_user_password_error_handler(error: AuthUserInvalidPasswordException) -> Response:
    """Custom AuthUserInvalidPasswordException handler return http Response with error message."""
    STATUS_CODE = HttpStatusCodeConstants.HTTP_401_UNAUTHORIZED.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': [],
            'errors': {'message': str(error)},
        }
    )
    return make_response(jsonify(response), STATUS_CODE)
