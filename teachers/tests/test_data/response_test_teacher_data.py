from unittest.mock import ANY

from common.tests.test_data.teachers import request_test_teacher_data

RESPONSE_TEACHER_TEST_DATA = {
    'id': ANY,
    'card_id': 'UNI-0000001',
    'qualification': request_test_teacher_data.ADD_TEACHER_TEST_DATA['qualification'],
    'working_since': request_test_teacher_data.ADD_TEACHER_TEST_DATA['working_since'],
}
RESPONSE_TEACHERS_TEST_DATA = [RESPONSE_TEACHER_TEST_DATA]
RESPONSE_TEACHER_NOT_FOUND = {'message': f'Teacher with id: {request_test_teacher_data.DUMMY_TEACHER_UUID} not found.'}
RESPONSE_TEACHER_INVALID_PAYLOAD = {
    'qualification': ['Missing data for required field.'],
    'working_since': ['Missing data for required field.'],
}
RESPONSE_TEACHER_UPDATE_TEST_DATA = {
    'id': ANY,
    'card_id': 'UNI-0000001',
    'qualification': request_test_teacher_data.UPDATE_TEACHER_TEST_DATA['qualification'],
    'working_since': request_test_teacher_data.UPDATE_TEACHER_TEST_DATA['working_since'],
}
RESPONSE_TEACHER_UNAUTHORIZED_UPDATE = {'msg': 'User claims verification failed'}
RESPONSE_TEACHER_DELETE = None
RESPONSE_TEACHER_UNAUTHORIZED_DELETE = {'msg': 'User claims verification failed'}
RESPONSE_USER_ALREADY_STUDENT = {
    'message': 'Teacher with id: {first_id} can not be created, because a Student with id: {second_id} already exists.'
}
