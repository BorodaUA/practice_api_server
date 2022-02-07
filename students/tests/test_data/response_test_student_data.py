from unittest.mock import ANY

from common.tests.test_data.students import request_test_student_data

RESPONSE_STUDENT_TEST_DATA = {
    'id': ANY,
    'card_id': 'STU-0000001',
    'student_since': request_test_student_data.ADD_STUDENT_TEST_DATA['student_since'],
}
RESPONSE_STUDENTS_TEST_DATA = [RESPONSE_STUDENT_TEST_DATA]
RESPONSE_STUDENT_NOT_FOUND = {'message': f'Student with id: {request_test_student_data.DUMMY_STUDENT_UUID} not found.'}
RESPONSE_STUDENT_INVALID_PAYLOAD = {
    'working_since': ['Missing data for required field.'],
}
RESPONSE_STUDENT_UPDATE_TEST_DATA = {
    'id': ANY,
    'card_id': 'UNI-0000001',
    'student_since': request_test_student_data.UPDATE_STUDENT_TEST_DATA['student_since'],
}
RESPONSE_STUDENT_UNAUTHORIZED_UPDATE = {'msg': 'User claims verification failed'}
RESPONSE_STUDENT_DELETE = None
RESPONSE_STUDENT_UNAUTHORIZED_DELETE = {'msg': 'User claims verification failed'}
