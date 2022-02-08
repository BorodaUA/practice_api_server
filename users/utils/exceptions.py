from flask import Response, jsonify, make_response

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema


class UserNotFoundError(Exception):
    pass


def user_not_found_error_handler(error: UserNotFoundError) -> Response:
    """Custom UserNotFoundError handler return http Response with error message."""
    STATUS_CODE = HttpStatusCodeConstants.HTTP_404_NOT_FOUND.value
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
