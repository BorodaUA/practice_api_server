from flask import Response, jsonify, make_response

from common.constants.http import HttpStatusCodeConstants


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
    return make_response(
        jsonify({'message': str(error)}),
        HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value,
    )


def teacher_not_found_error_handler(error: TeacherNotFoundError) -> Response:
    """Custom TeacherNotFoundError handler.

    Args:
        error: raised custom TeacherNotFoundError.

    Returns:
    http Response with formatted error message.
    """
    return make_response(
        jsonify({'message': str(error)}),
        HttpStatusCodeConstants.HTTP_404_NOT_FOUND.value,
    )
