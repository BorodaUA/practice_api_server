from unittest.mock import ANY

from common.tests.test_data.students import request_test_student_data

RESPONSE_STUDENT_TEST_DATA = {
    'id': ANY,
    'card_id': 'STU-0000001',
    'student_since': request_test_student_data.ADD_STUDENT_TEST_DATA['student_since'],
}
# GET
RESPONSE_STUDENTS_EMPTY_DB = {'data': [], 'errors': [], 'status': {'code': 200}}
RESPONSE_GET_STUDENT = {
    'data': RESPONSE_STUDENT_TEST_DATA,
    'errors': [],
    'status': {'code': 200},
}
RESPONSE_GET_STUDENTS = {
    'data': [RESPONSE_STUDENT_TEST_DATA],
    'errors': [],
    'status': {'code': 200},
}
# POST
RESPONSE_POST_STUDENT = {
    'data': RESPONSE_STUDENT_TEST_DATA,
    'errors': [],
    'status': {'code': 201},
}
# PUT
RESPONSE_STUDENT_UPDATE_TEST_DATA = {
    'data': {
        'id': ANY,
        'card_id': 'STU-0000001',
        'student_since': request_test_student_data.UPDATE_STUDENT_TEST_DATA['student_since'],
    },
    'errors': [],
    'status': {'code': 200},
}
# ERRORS
RESPONSE_STUDENT_NOT_FOUND = {
    'data': [],
    'errors': {'message': f'Student with id: {request_test_student_data.DUMMY_STUDENT_UUID} not found.'},
    'status': {'code': 404}
}
RESPONSE_STUDENT_INVALID_PAYLOAD = {
    'data': [],
    'errors': {
        'message': {'student_since': ['Missing data for required field.']}
    },
    'status': {'code': 400}
}
RESPONSE_STUDENT_UNAUTHORIZED_UPDATE = {'msg': 'User claims verification failed'}
RESPONSE_STUDENT_DELETE = None
RESPONSE_STUDENT_UNAUTHORIZED_DELETE = {'msg': 'User claims verification failed'}
RESPONSE_USER_ALREADY_TEACHER = {
    'data': [],
    'errors': {
        'message': (
            'Student with id: {first_id} can not be created, '
            'because a Teacher with id: {second_id} already exists.'
        )
    },
    'status': {'code': 400}
}
