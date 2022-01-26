from flask import Response, jsonify, make_response

from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from common.constants.http import HttpStatusCodeConstants


class UserNotFoundError(Exception):
    pass


def user_validation_error_handler(error: ValidationError) -> Response:
    """Custom ValidationError handler return http Response with error message."""
    return make_response(jsonify(error.messages), HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value)


def user_not_found_error_handler(error: UserNotFoundError) -> Response:
    """Custom UserNotFoundError handler return http Response with error message."""
    return make_response(jsonify({'message': str(error)}), HttpStatusCodeConstants.HTTP_404_NOT_FOUND.value)


def user_duplicate_error_handler(error: IntegrityError) -> Response:
    """Custom IntegrityError handler return http Response with error message."""
    return make_response(
        jsonify({'message': error.orig.pgerror}),
        HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value,
    )
