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


class PostTeachersTestCase(TestMixin, TestCase):
    """Tests for POST '/teachers' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('teachers.post_teachers')

    def test_post_teachers_valid_payload(self) -> None:
        """Test POST '/teachers' endpoint with valid json payload."""
        db_user = self.add_user_to_db()
        payload_data = request_test_teacher_data.ADD_TEACHER_TEST_DATA
        payload_data['id'] = db_user.id
        response = self.client.post(self.url, json=payload_data)
        response_data = response.get_json()
        expected_result = response_test_teacher_data.RESPONSE_TEACHER_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_201_CREATED.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Teacher).count())

    def test_post_teachers_invalid_json_payload(self) -> None:
        """Test POST '/teachers' endpoint with invalid empty json payload."""
        response = self.client.post(self.url, json=request_test_teacher_data.ADD_TEACHER_EMPTY_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_teacher_data.RESPONSE_TEACHER_INVALID_PAYLOAD
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Teacher).count())

    def test_post_teachers_user_already_registered_as_student(self) -> None:
        """Test POST '/teachers' endpoint with user id already registered as student."""
        db_student = self.add_student_to_db()
        payload_data = request_test_teacher_data.ADD_TEACHER_TEST_DATA
        payload_data['id'] = db_student.id
        response = self.client.post(self.url, json=payload_data)
        response_data = response.get_json()
        response_test_teacher_data.RESPONSE_USER_ALREADY_STUDENT['message'] = (
            response_test_teacher_data.RESPONSE_USER_ALREADY_STUDENT['message'].format(
                first_id=db_student.id, second_id=db_student.id,
            )
        )
        expected_result = response_test_teacher_data.RESPONSE_USER_ALREADY_STUDENT
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Teacher).count())


class PutTeachersTestCase(TestMixin, TestCase):
    """Tests for PUT '/teachers/{id}' endpoint."""

    def test_put_teachers_valid_payload_and_user_authenticated(self) -> None:
        """Test PUT '/teachers/{id}' endpoint with valid payload and valid auth cookies."""
        db_teacher = self.add_authenticated_teacher()
        url = url_for('teachers.put_teacher', id=db_teacher.id)
        response = self.client.put(url, json=request_test_teacher_data.UPDATE_TEACHER_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_teacher_data.RESPONSE_TEACHER_UPDATE_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Teacher).count())

    def test_put_teachers_updating_other_teacher_data(self) -> None:
        """Test PUT '/teachers/{id}' endpoint updating other's teacher information."""
        self.add_authenticated_teacher()
        random_db_teacher = self.add_random_teacher_to_db()
        url = url_for('teachers.put_teacher', id=random_db_teacher.id)
        response = self.client.put(url, json=request_test_teacher_data.UPDATE_TEACHER_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_teacher_data.RESPONSE_TEACHER_UNAUTHORIZED_UPDATE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(2, self.db_session.query(Teacher).count())


class DeleteTeachersTestCase(TestMixin, TestCase):
    """Tests for DELETE '/teachers/{id}' endpoint."""

    def test_delete_teachers_teacher_authenticated_and_deleting_himself(self) -> None:
        """Test DELETE '/teachers/{id}' endpoint with valid auth cookies, teacher deleting himself."""
        db_teacher = self.add_authenticated_teacher()
        url = url_for('teachers.delete_teacher', id=db_teacher.id)
        self.assertEqual(1, self.db_session.query(Teacher).count())
        response = self.client.delete(url)
        response_data = response.get_json()
        expected_result = response_test_teacher_data.RESPONSE_TEACHER_DELETE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_204_NO_CONTENT.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Teacher).count())

    def test_delete_teachers_deleting_other_teacher_data(self) -> None:
        """Test DELETE '/teachers/{id}' endpoint deleting other's teacher information."""
        self.add_authenticated_teacher()
        random_db_teacher = self.add_random_teacher_to_db()
        url = url_for('teachers.delete_teacher', id=random_db_teacher.id)
        response = self.client.delete(url)
        response_data = response.get_json()
        expected_result = response_test_teacher_data.RESPONSE_TEACHER_UNAUTHORIZED_DELETE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(2, self.db_session.query(Teacher).count())
