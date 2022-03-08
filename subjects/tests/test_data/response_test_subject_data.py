from unittest.mock import ANY

from common.tests.test_data.subjects import request_test_subject_data

RESPONSE_SUBJECT_TEST_DATA = {
    'title': request_test_subject_data.ADD_SUBJECT_TEST_DATA['title'],
    'code': request_test_subject_data.ADD_SUBJECT_TEST_DATA['code'],
    'id': ANY,
}
# GET
RESPONSE_SUBJECT_EMPTY_DB = {'data': [], 'errors': [], 'status': {'code': 200}}
RESPONSE_GET_SUBJECTS = {
    'data': [RESPONSE_SUBJECT_TEST_DATA],
    'errors': [],
    'status': {'code': 200},
}
RESPONSE_GET_SUBJECT = {
    'data': RESPONSE_SUBJECT_TEST_DATA,
    'errors': [],
    'status': {'code': 200},
}
# POST
RESPONSE_POST_SUBJECT = {
    'data': RESPONSE_SUBJECT_TEST_DATA,
    'errors': [],
    'status': {'code': 201},
}
# PUT
RESPONSE_SUBJECT_UPDATE_TEST_DATA = {
    'data': {
        'id': ANY,
        'title': request_test_subject_data.UPDATE_SUBJECT_TEST_DATA['title'],
        'code': request_test_subject_data.UPDATE_SUBJECT_TEST_DATA['code'],
    },
    'errors': [],
    'status': {'code': 200},
}
# DELETE
RESPONSE_SUBJECT_DELETE = None
# ERRORS
RESPONSE_SUBJECT_NOT_FOUND = {
    'data': [],
    'errors': {'message': f'Subject with id: {request_test_subject_data.DUMMY_SUBJECT_UUID} not found.'},
    'status': {'code': 404},
}
RESPONSE_SUBJECT_INVALID_PAYLOAD = {
    'data': [],
    'errors': {
        'message': {
            'title': ['Missing data for required field.'],
            'code': ['Missing data for required field.'],
            'teacher_id': ['Missing data for required field.'],
        },
    },
    'status': {'code': 400}
}
RESPONSE_SUBJECT_UNAUTHORIZED_UPDATE = {'msg': 'User claims verification failed'}
RESPONSE_SUBJECT_UNAUTHORIZED_DELETE = {'msg': 'User claims verification failed'}
