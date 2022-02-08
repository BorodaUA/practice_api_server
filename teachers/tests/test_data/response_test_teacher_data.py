from unittest.mock import ANY

from common.tests.test_data.teachers import request_test_teacher_data

RESPONSE_TEACHER_TEST_DATA = {
    'id': ANY,
    'card_id': 'UNI-0000001',
    'qualification': request_test_teacher_data.ADD_TEACHER_TEST_DATA['qualification'],
    'working_since': request_test_teacher_data.ADD_TEACHER_TEST_DATA['working_since'],
}
# GET
RESPONSE_TEACHERS_EMPTY_DB = {'data': [], 'errors': [], 'status': {'code': 200}}
RESPONSE_GET_TEACHER = {
    'data': RESPONSE_TEACHER_TEST_DATA,
    'errors': [],
    'status': {'code': 200}
}
RESPONSE_GET_TEACHERS = {
    'data': [RESPONSE_TEACHER_TEST_DATA],
    'errors': [],
    'status': {'code': 200}
}
# POST
RESPONSE_POST_TEACHERS = {
    'data': RESPONSE_TEACHER_TEST_DATA,
    'errors': [],
    'status': {'code': 201}
}
# PUT
RESPONSE_TEACHER_UPDATE_TEST_DATA = {
    'data': {
        'id': ANY,
        'card_id': 'UNI-0000001',
        'qualification': request_test_teacher_data.UPDATE_TEACHER_TEST_DATA['qualification'],
        'working_since': request_test_teacher_data.UPDATE_TEACHER_TEST_DATA['working_since'],
    },
    'errors': [],
    'status': {'code': 200}
}
# ERRORS
RESPONSE_TEACHER_NOT_FOUND = {
    'data': [],
    'errors': {'message': f'Teacher with id: {request_test_teacher_data.DUMMY_TEACHER_UUID} not found.'},
    'status': {'code': 404}
}
RESPONSE_TEACHER_INVALID_PAYLOAD = {
    'data': [],
    'errors': {
        'message': {
            'qualification': ['Missing data for required field.'],
            'working_since': ['Missing data for required field.'],
        },
    },
    'status': {'code': 400}
}
RESPONSE_USER_ALREADY_STUDENT = {
    'data': [],
    'errors': {
        'message': (
            'Teacher with id: {first_id} can not be created, '
            'because a Student with id: {second_id} already exists.'
        )
    },
    'status': {'code': 400}
}
RESPONSE_TEACHER_UNAUTHORIZED_UPDATE = {'msg': 'User claims verification failed'}
RESPONSE_TEACHER_DELETE = None
RESPONSE_TEACHER_UNAUTHORIZED_DELETE = {'msg': 'User claims verification failed'}
