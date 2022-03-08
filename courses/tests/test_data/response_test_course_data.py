from unittest.mock import ANY

from common.tests.test_data.courses import request_test_course_data
from subjects.tests.test_data import response_test_subject_data
from teachers.tests.test_data import response_test_teacher_data

RESPONSE_COURSE_TEST_DATA = {
    'subject': response_test_subject_data.RESPONSE_SUBJECT_TEST_DATA,
    'start_date': request_test_course_data.ADD_COURSE_TEST_DATA['start_date'],
    'end_date': request_test_course_data.ADD_COURSE_TEST_DATA['end_date'],
    'id': ANY,
    'students': [],
    'teacher': response_test_teacher_data.RESPONSE_TEACHER_TEST_DATA,
}
# GET
RESPONSE_COURSES_EMPTY_DB = {'data': [], 'errors': [], 'status': {'code': 200}}
RESPONSE_GET_COURSES = {
    'data': [RESPONSE_COURSE_TEST_DATA],
    'errors': [],
    'status': {'code': 200},
}
RESPONSE_GET_COURSE = {
    'data': RESPONSE_COURSE_TEST_DATA,
    'errors': [],
    'status': {'code': 200},
}
# POST
RESPONSE_POST_COURSE = {
    'data': RESPONSE_COURSE_TEST_DATA,
    'errors': [],
    'status': {'code': 201},
}
# PUT
RESPONSE_COURSE_UPDATE_TEST_DATA = {
    'data': {
        'start_date': request_test_course_data.UPDATE_COURSE_TEST_DATA['start_date'],
        'end_date': request_test_course_data.UPDATE_COURSE_TEST_DATA['end_date'],
        'id': ANY,
        'students': [],
        'teacher': response_test_teacher_data.RESPONSE_TEACHER_TEST_DATA,
        'subject': response_test_subject_data.RESPONSE_SUBJECT_TEST_DATA,
    },
    'errors': [],
    'status': {'code': 200},
}
# DELETE
RESPONSE_COURSE_DELETE = None
# ERRORS
RESPONSE_COURSE_NOT_FOUND = {
    'data': [],
    'errors': {'message': f'Course with id: {request_test_course_data.DUMMY_COURSE_UUID} not found.'},
    'status': {'code': 404},
}
RESPONSE_COURSE_INVALID_PAYLOAD = {
    'data': [],
    'errors': {
        'message': {
            'start_date': ['Missing data for required field.'],
            'end_date': ['Missing data for required field.'],
            'teacher_id': ['Missing data for required field.'],
            'subject_id': ['Missing data for required field.'],
        },
    },
    'status': {'code': 400}
}
RESPONSE_COURSE_UNAUTHORIZED_UPDATE = {'msg': 'User claims verification failed'}
RESPONSE_COURSE_UNAUTHORIZED_DELETE = {'msg': 'User claims verification failed'}
