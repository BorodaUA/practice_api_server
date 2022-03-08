from unittest.mock import ANY

from common.tests.test_data.courses import request_test_course_data
from courses.tests.test_data import response_test_course_data
from students.tests.test_data import response_test_student_data

# GET
RESPONSE_COURSE_STUDENTS_EMPTY_DB = {'data': [], 'errors': [], 'status': {'code': 200}}
# DELETE
RESPONSE_COURSE_STUDENTS_DELETE = {
    'data': {
        'end_date': ANY,
        'id': ANY,
        'start_date': ANY,
        'students': [],
        'subject': {
            'code': ANY,
            'id': ANY,
            'title': ANY,
        },
        'teacher': {
            'card_id': 'UNI-0000001',
            'id': ANY,
            'qualification': 'Biology Teacher',
            'working_since': '2010-05-10',
        }
    },
    'errors': [],
    'status': {'code': 200}
}
# ERRORS
RESPONSE_COURSE_STUDENT_NOT_FOUND = {
    'data': [],
    'errors': {
        'message': (
            'Student with id: {student_id} '
            'not found in Course with id: {course_id}.'
        )
    },
    'status': {'code': 404},
}
RESPONSE_COURSE_STUDENT_INVALID_PAYLOAD = {
    'data': [],
    'errors': {
        'message': {
            'id': ['Missing data for required field.'],
        },
    },
    'status': {'code': 400}
}
RESPONSE_COURSE_STUDENT_UNAUTHORIZED_DELETE = {'msg': 'User claims verification failed'}
