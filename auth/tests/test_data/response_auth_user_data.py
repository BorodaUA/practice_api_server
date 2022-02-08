from unittest.mock import ANY

RESPONSE_VALID_LOGIN_DATA = {
    'data': {
        'access_token': ANY,
        'refresh_token': ANY,
    },
    'errors': [],
    'status': {'code': 200},
}
RESPONSE_INVALID_LOGIN_PASSWORD = {
    'data': [],
    'errors': {'message': 'Incorrect username or password.'},
    'status': {'code': 401},
}
RESPONSE_NO_ACCESS_COOKIES = {'msg': 'Missing cookie "access_token_cookie"'}
RESPONSE_USER_LOGOUT_MSG = {
    'data': {'message': 'User successfully logged out.'},
    'errors': [],
    'status': {'code': 200},
}
