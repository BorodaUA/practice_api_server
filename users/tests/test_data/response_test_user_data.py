from unittest.mock import ANY

from common.tests.test_data.users import request_test_user_data

RESPONSE_USER_TEST_DATA = {
    'id': ANY,
    'username': 'test_john',
    'first_name': 'john',
    'last_name': 'bar',
    'email': 'test_john@john.com',
    'phone_number': '+380991112233',
}
# GET
RESPONSE_USERS_EMPTY_DB = {'data': [], 'errors': [], 'status': {'code': 200}}
RESPONSE_GET_USER = {
    'data': RESPONSE_USER_TEST_DATA,
    'errors': [],
    'status': {'code': 200}
}
RESPONSE_GET_USERS = {
    'data': [RESPONSE_USER_TEST_DATA],
    'errors': [],
    'status': {'code': 200}
}
# POST
RESPONSE_POST_USER = {
    'data': RESPONSE_USER_TEST_DATA,
    'errors': [],
    'status': {'code': 201}
}
# PUT
RESPONSE_USER_UPDATE_TEST_DATA = {
    'data': {
        'id': ANY,
        'username': request_test_user_data.UPDATE_USER_TEST_DATA['username'],
        'first_name': request_test_user_data.UPDATE_USER_TEST_DATA['first_name'],
        'last_name': request_test_user_data.UPDATE_USER_TEST_DATA['last_name'],
        'email': request_test_user_data.UPDATE_USER_TEST_DATA['email'],
        'phone_number': request_test_user_data.UPDATE_USER_TEST_DATA['phone_number'],
    },
    'errors': [],
    'status': {'code': 200}
}
# ERRORS
RESPONSE_USER_NOT_FOUND = {
    'data': [],
    'errors': {'message': f'User with id: {request_test_user_data.DUMMY_USER_UUID} not found.'},
    'status': {'code': 404}
}
RESPONSE_USER_INVALID_PAYLOAD = {
    'data': [],
    'errors': {
        'message': {
            'email': ['Missing data for required field.'],
            'password': ['Missing data for required field.'],
            'phone_number': ['Missing data for required field.'],
            'username': ['Missing data for required field.'],
        },
    },
    'status': {'code': 400}
}
RESPONSE_USER_DUPLICATE_USERNAME = {
    'data': [],
    'errors': {
        'message': f'User with username: {request_test_user_data.ADD_USER_TEST_DATA["username"]} already exists.'
    },
    'status': {'code': 400}
}
RESPONSE_USER_UNAUTHORIZED_UPDATE = {'msg': 'User claims verification failed'}
RESPONSE_USER_DELETE = None
