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
