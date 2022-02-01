from unittest.mock import ANY

RESPONSE_VALID_LOGIN_DATA = {
    'access_token': ANY,
    'refresh_token': ANY,
}
RESPONSE_INVALID_LOGIN_PASSWORD = {'message': 'Incorrect username or password.'}
RESPONSE_NO_ACCESS_COOKIES = {'msg': 'Missing cookie "access_token_cookie"'}
RESPONSE_USER_LOGOUT_MSG = {'message': 'User successfully logged out.'}
