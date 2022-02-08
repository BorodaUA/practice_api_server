from flask import Response, jsonify, make_response

from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema


class TeacherExistsError(Exception):
    pass


class StudentNotFoundError(Exception):
    pass


def teacher_exists_error_handler(error: TeacherExistsError) -> Response:
    """Custom TeacherExistsError handler.

    Args:
        error: raised custom TeacherExistsError.

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


def student_not_found_error_handler(error: StudentNotFoundError) -> Response:
    """Custom StudentNotFoundError handler.

    Args:
        error: raised custom StudentNotFoundError.

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
