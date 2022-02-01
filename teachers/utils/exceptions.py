from flask import Response, jsonify, make_response

from common.constants.http import HttpStatusCodeConstants


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
