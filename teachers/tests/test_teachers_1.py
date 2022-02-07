from unittest import TestCase

from flask import url_for

from common.constants.http import HttpStatusCodeConstants
from common.tests.generic import TestMixin
from common.tests.test_data.teachers import request_test_teacher_data
from teachers.models import Teacher
from teachers.tests.test_data import response_test_teacher_data


class GetTeachersTestCase(TestMixin, TestCase):
    """Tests for GET '/teachers' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('teachers.get_teachers')

    def test_get_teachers_empty_db(self) -> None:
        """Test GET '/teachers' endpoint with no teacher's data added to the db."""
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = []
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Teacher).count())

    def test_get_teachers_test_data_in_db(self) -> None:
        """Test GET '/teachers' endpoint with teacher's test data added to the db."""
        self.add_teacher_to_db()
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = response_test_teacher_data.RESPONSE_TEACHERS_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Teacher).count())


class GetTeacherTestCase(TestMixin, TestCase):
    """Tests for GET '/teachers/{id}' endpoint."""

    def test_get_teacher_no_test_data_in_db(self) -> None:
        """Test GET '/teachers/{id}' endpoint with no teacher's test data added to the db."""
        url = url_for('teachers.get_teacher', id=request_test_teacher_data.DUMMY_TEACHER_UUID)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_teacher_data.RESPONSE_TEACHER_NOT_FOUND
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_404_NOT_FOUND.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Teacher).count())

    def test_get_teacher_test_data_in_db(self) -> None:
        """Test GET '/teacher/{id}' endpoint with teacher's test data added to the db."""
        db_teacher = self.add_teacher_to_db()
        url = url_for('teachers.get_teacher', id=db_teacher.id)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_teacher_data.RESPONSE_TEACHER_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Teacher).count())
