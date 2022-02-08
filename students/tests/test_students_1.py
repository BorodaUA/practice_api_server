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
        expected_result = response_test_student_data.RESPONSE_STUDENTS_EMPTY_DB
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Student).count())

    def test_get_students_test_data_in_db(self) -> None:
        """Test GET '/students' endpoint with student's test data added to the db."""
        self.add_student_to_db()
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = response_test_student_data.RESPONSE_GET_STUDENTS
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
        expected_result = response_test_student_data.RESPONSE_GET_STUDENT
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Student).count())


class PostStudentsTestCase(TestMixin, TestCase):
    """Tests for POST '/students' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('students.post_students')

    def test_post_students_valid_payload(self) -> None:
        """Test POST '/students' endpoint with valid json payload."""
        db_user = self.add_user_to_db()
        payload_data = request_test_student_data.ADD_STUDENT_TEST_DATA
        payload_data['id'] = db_user.id
        response = self.client.post(self.url, json=payload_data)
        response_data = response.get_json()
        expected_result = response_test_student_data.RESPONSE_POST_STUDENT
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_201_CREATED.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Student).count())

    def test_post_students_invalid_json_payload(self) -> None:
        """Test POST '/students' endpoint with invalid empty json payload."""
        response = self.client.post(self.url, json=request_test_student_data.ADD_STUDENT_EMPTY_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_student_data.RESPONSE_STUDENT_INVALID_PAYLOAD
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Student).count())

    def test_post_students_user_already_registered_as_teacher(self) -> None:
        """Test POST '/students' endpoint with user id already registered as teacher."""
        db_teacher = self.add_teacher_to_db()
        payload_data = request_test_student_data.ADD_STUDENT_TEST_DATA
        payload_data['id'] = db_teacher.id
        response = self.client.post(self.url, json=payload_data)
        response_data = response.get_json()
        response_test_student_data.RESPONSE_USER_ALREADY_TEACHER['errors']['message'] = (
            response_test_student_data.RESPONSE_USER_ALREADY_TEACHER['errors']['message'].format(
                first_id=db_teacher.id, second_id=db_teacher.id,
            )
        )
        expected_result = response_test_student_data.RESPONSE_USER_ALREADY_TEACHER
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Student).count())


class PutStudentTestCase(TestMixin, TestCase):
    """Tests for PUT '/students/{id}' endpoint."""

    def test_put_student_valid_payload_and_user_authenticated(self) -> None:
        """Test PUT '/students/{id}' endpoint with valid payload and auth cookies."""
        db_student = self.add_authenticated_student()
        url = url_for('students.put_student', id=db_student.id)
        response = self.client.put(url, json=request_test_student_data.UPDATE_STUDENT_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_student_data.RESPONSE_STUDENT_UPDATE_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Student).count())

    def test_put_student_updating_other_student_data(self) -> None:
        """Test PUT '/students/{id}' endpoint updating other's student information."""
        self.add_authenticated_student()
        random_db_student = self.add_random_student_to_db()
        url = url_for('students.put_student', id=random_db_student.id)
        response = self.client.put(url, json=request_test_student_data.UPDATE_STUDENT_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_student_data.RESPONSE_STUDENT_UNAUTHORIZED_UPDATE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(2, self.db_session.query(Student).count())


class DeleteStudentTestCase(TestMixin, TestCase):
    """Tests for DELETE '/students/{id}' endpoint."""

    def test_delete_student_authenticated_and_deleting_himself(self) -> None:
        """Test DELETE '/students/{id}' endpoint with valid auth cookies, student deleting himself."""
        db_student = self.add_authenticated_student()
        url = url_for('students.delete_student', id=db_student.id)
        self.assertEqual(1, self.db_session.query(Student).count())
        response = self.client.delete(url)
        response_data = response.get_json()
        expected_result = response_test_student_data.RESPONSE_STUDENT_DELETE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_204_NO_CONTENT.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Student).count())

    def test_delete_student_deleting_other_student_data(self) -> None:
        """Test DELETE '/students/{id}' endpoint deleting other's student information."""
        self.add_authenticated_student()
        random_db_student = self.add_random_student_to_db()
        url = url_for('students.delete_student', id=random_db_student.id)
        response = self.client.delete(url)
        response_data = response.get_json()
        expected_result = response_test_student_data.RESPONSE_STUDENT_UNAUTHORIZED_DELETE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(2, self.db_session.query(Student).count())
