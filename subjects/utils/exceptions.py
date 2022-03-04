from flask import Response, jsonify, make_response

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema


class SubjectNotFoundError(Exception):
    pass


def subject_not_found_error_handler(error: SubjectNotFoundError) -> Response:
    """Custom SubjectNotFoundError handler.

    Args:
        error: raised custom SubjectNotFoundError.

    Returns:
    http Response with formatted error message.
    """
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
