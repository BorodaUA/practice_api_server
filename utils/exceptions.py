import re

from flask import Response, jsonify, make_response

from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from common.constants.exceptions import SqlalchemyExceptionConstants
from common.constants.http import HttpStatusCodeConstants
from common.schemas.response import ResponseBaseSchema


def parse_integrity_error(error: IntegrityError) -> tuple:
    """Get sqlalchemy IntegrityError and parse it to get data from the error.

    Args:
        error: raised sqlalchemy IntegrityError.

    Returns:
    tuple with data: table_name, field where error occurred and value of that field.
    """
    table_name = re.search(
        SqlalchemyExceptionConstants.INTEGRITY_ERROR_TABLE_NAME_REGEX.value,
        error.orig.pgerror,
    ).group(1)
    table_name = table_name.split('_')[0][:-1].capitalize()
    field, value = re.findall(
        SqlalchemyExceptionConstants.INTEGRITY_ERROR_FIELD_VALUE_REGEX.value,
        error.orig.pgerror,
    )
    return table_name, field, value


def integrity_error_handler(error: IntegrityError) -> Response:
    """Custom IntegrityError handler return http Response with error message."""
    ERROR_MESSAGE = get_error_message(error)
    STATUS_CODE = HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': [],
            'errors': {'message': ERROR_MESSAGE},
        }
    )
    return make_response(jsonify(response), STATUS_CODE)


def get_error_message(error: IntegrityError) -> str:
    """Get formatted error message bases of error.orig type.

    Args:
        error: raised sqlalchemy IntegrityError.

    Returns:
    Properly formatted error message.
    """
    table_name, field, value = parse_integrity_error(error=error)
    SQLALCHEMY_INTEGRITY_ERROR_MAP = {
        'UniqueViolation': f'{table_name} with {field}: {value} already exists.',
        'ForeignKeyViolation': f'Foreign key violation {field}: {value} is not present in table.',
    }
    return SQLALCHEMY_INTEGRITY_ERROR_MAP[error.orig.__class__.__name__]


def marshmallow_validation_error_handler(error: ValidationError) -> Response:
    """Custom marshmallow ValidationError handler return http Response with error message."""
    STATUS_CODE = HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value
    response = ResponseBaseSchema().load(
        {
            'status': {
                'code': STATUS_CODE,
            },
            'data': [],
            'errors': {'message': error.messages},
        }
    )
    return make_response(jsonify(response), STATUS_CODE)
