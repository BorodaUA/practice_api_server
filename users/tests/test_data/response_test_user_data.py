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
RESPONSE_USERS_TEST_DATA = [RESPONSE_USER_TEST_DATA]
RESPONSE_USER_NOT_FOUND = {'message': f'User with id: {request_test_user_data.DUMMY_USER_UUID} not found.'}
RESPONSE_USER_INVALID_PAYLOAD = {
    'email': ['Missing data for required field.'],
    'password': ['Missing data for required field.'],
    'phone_number': ['Missing data for required field.'],
    'username': ['Missing data for required field.'],
}
RESPONSE_USER_DUPLICATE_USERNAME = {
    'message': 'ERROR:  duplicate key value violates unique constraint '
    '"Users_username_key"\n'
    f'DETAIL:  Key (username)=({request_test_user_data.ADD_USER_TEST_DATA["username"]}) already exists.\n'
}
RESPONSE_USER_UPDATE_TEST_DATA = {
    'id': ANY,
    'username': request_test_user_data.UPDATE_USER_TEST_DATA['username'],
    'first_name': request_test_user_data.UPDATE_USER_TEST_DATA['first_name'],
    'last_name': request_test_user_data.UPDATE_USER_TEST_DATA['last_name'],
    'email': request_test_user_data.UPDATE_USER_TEST_DATA['email'],
    'phone_number': request_test_user_data.UPDATE_USER_TEST_DATA['phone_number'],
}
RESPONSE_USER_UNAUTHORIZED_UPDATE = {'msg': 'User claims verification failed'}
RESPONSE_USER_DELETE = None
