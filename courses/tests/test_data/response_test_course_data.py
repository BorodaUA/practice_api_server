from unittest.mock import ANY

from common.tests.test_data.courses import request_test_course_data
from teachers.tests.test_data import response_test_teacher_data

RESPONSE_TEACHER_TEST_DATA = {
    'title': request_test_course_data.ADD_COURSE_TEST_DATA['title'],
    'code': request_test_course_data.ADD_COURSE_TEST_DATA['code'],
    'start_date': request_test_course_data.ADD_COURSE_TEST_DATA['start_date'],
    'end_date': request_test_course_data.ADD_COURSE_TEST_DATA['end_date'],
    'id': ANY,
    'students': [],
    'teacher': response_test_teacher_data.RESPONSE_TEACHER_TEST_DATA,
}
# GET
RESPONSE_COURSES_EMPTY_DB = {'data': [], 'errors': [], 'status': {'code': 200}}
RESPONSE_GET_COURSES = {
    'data': [RESPONSE_TEACHER_TEST_DATA],
    'errors': [],
    'status': {'code': 200},
}
RESPONSE_GET_COURSE = {
    'data': RESPONSE_TEACHER_TEST_DATA,
    'errors': [],
    'status': {'code': 200},
}
# ERRORS
RESPONSE_COURSE_NOT_FOUND = {
    'data': [],
    'errors': {'message': f'Course with id: {request_test_course_data.DUMMY_COURSE_UUID} not found.'},
    'status': {'code': 404},
}
