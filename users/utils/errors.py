from flask import Response, jsonify, make_response

from marshmallow.exceptions import ValidationError

from common.constants.http import HttpStatusCodeConstants


def user_validation_error_handler(error: ValidationError) -> Response:
    """Custom ValidationError handler return http Response with error message."""
    return make_response(jsonify(error.messages), HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value)
