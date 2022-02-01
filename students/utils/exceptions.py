from flask import Response, jsonify, make_response

from common.constants.http import HttpStatusCodeConstants


class TeacherExistsError(Exception):
    pass


def teacher_exists_error_handler(error: TeacherExistsError) -> Response:
    """Custom TeacherExistsError handler.

    Args:
        error: raised custom TeacherExistsError.

    Returns:
    http Response with formatted error message.
    """
    return make_response(
        jsonify({'message': str(error)}),
        HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value,
    )
