from flask import Response, jsonify, make_response

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema


class CourseNotFoundError(Exception):
    pass


def course_not_found_error_handler(error: CourseNotFoundError) -> Response:
    """Custom CourseNotFoundError handler.

    Args:
        error: raised custom CourseNotFoundError.

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
