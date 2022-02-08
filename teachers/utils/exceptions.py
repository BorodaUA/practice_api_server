from flask import Response, jsonify, make_response

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema


class TeacherNotFoundError(Exception):
    pass


class StudentExistsError(Exception):
    pass


def student_exists_error_handler(error: StudentExistsError) -> Response:
    """Custom StudentExistsError handler.

    Args:
        error: raised custom StudentExistsError.

    Returns:
    http Response with formatted error message.
    """
    STATUS_CODE = HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value
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


def teacher_not_found_error_handler(error: TeacherNotFoundError) -> Response:
    """Custom TeacherNotFoundError handler.

    Args:
        error: raised custom TeacherNotFoundError.

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
