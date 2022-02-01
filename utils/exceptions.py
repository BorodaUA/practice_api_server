import re

from flask import Response, jsonify, make_response

from sqlalchemy.exc import IntegrityError

from common.constants.exceptions import SqlalchemyExceptionConstants
from common.constants.http import HttpStatusCodeConstants


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


def duplicate_error_handler(error: IntegrityError) -> Response:
    """Custom IntegrityError handler return http Response with error message."""
    table_name, field, value = parse_integrity_error(error=error)
    DUPLICATE_ERROR_MESSAGE = f'{table_name} with {field}: {value} already exists.'
    return make_response(
        jsonify({'message': DUPLICATE_ERROR_MESSAGE}),
        HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value,
    )
