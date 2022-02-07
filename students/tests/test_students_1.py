from unittest import TestCase

from flask import url_for

from common.constants.http import HttpStatusCodeConstants
from common.tests.generic import TestMixin
from common.tests.test_data.students import request_test_student_data
from students.models import Student
from students.tests.test_data import response_test_student_data


class GetStudentsTestCase(TestMixin, TestCase):
    """Tests for GET '/students' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('students.get_students')

    def test_get_students_empty_db(self) -> None:
        """Test GET '/students' endpoint with no student's data added to the db."""
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = []
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Student).count())

    def test_get_students_test_data_in_db(self) -> None:
        """Test GET '/students' endpoint with student's test data added to the db."""
        self.add_student_to_db()
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = response_test_student_data.RESPONSE_STUDENTS_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Student).count())


class GetStudentTestCase(TestMixin, TestCase):
    """Tests for GET '/students/{id}' endpoint."""

    def test_get_student_no_test_data_in_db(self) -> None:
        """Test GET '/students/{id}' endpoint with no student's test data added to the db."""
        url = url_for('students.get_student', id=request_test_student_data.DUMMY_STUDENT_UUID)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_student_data.RESPONSE_STUDENT_NOT_FOUND
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_404_NOT_FOUND.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Student).count())

    def test_get_student_test_data_in_db(self) -> None:
        """Test GET '/students/{id}' endpoint with student's test data added to the db."""
        db_student = self.add_student_to_db()
        url = url_for('students.get_student', id=db_student.id)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_student_data.RESPONSE_STUDENT_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Student).count())
