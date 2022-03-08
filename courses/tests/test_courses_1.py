from unittest import TestCase

from flask import url_for

from common.constants.http import HttpStatusCodeConstants
from common.tests.generic import TestMixin
from common.tests.test_data.courses import request_test_course_data
from courses.models import Course
from courses.tests.test_data import response_test_course_data


class GetCoursesTestCase(TestMixin, TestCase):
    """Tests for GET '/courses' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('courses.get_courses')

    def test_get_courses_empty_db(self) -> None:
        """Test GET '/courses' endpoint with no course's data added to the db."""
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = response_test_course_data.RESPONSE_COURSES_EMPTY_DB
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Course).count())

    def test_get_courses_test_data_in_db(self) -> None:
        """Test GET '/courses' endpoint with course's test data added to the db."""
        self.add_course_to_db()
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = response_test_course_data.RESPONSE_GET_COURSES
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Course).count())


class GetCourseTestCase(TestMixin, TestCase):
    """Tests for GET '/courses/{id}' endpoint."""

    def test_get_course_no_test_data_in_db(self) -> None:
        """Test GET '/courses/{id}' endpoint with no course's test data added to the db."""
        url = url_for('courses.get_course', id=request_test_course_data.DUMMY_COURSE_UUID)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_course_data.RESPONSE_COURSE_NOT_FOUND
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_404_NOT_FOUND.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Course).count())

    def test_get_course_test_data_in_db(self) -> None:
        """Test GET '/courses/{id}' endpoint with course's test data added to the db."""
        db_course = self.add_course_to_db()
        url = url_for('courses.get_course', id=db_course.id)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_course_data.RESPONSE_GET_COURSE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Course).count())


class PostCoursesTestCase(TestMixin, TestCase):
    """Tests for POST '/courses' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('courses.post_courses')

    def test_post_courses_valid_payload(self) -> None:
        """Test POST '/courses' endpoint with valid json payload."""
        db_subject = self.add_subject_to_db()
        payload_data = request_test_course_data.ADD_COURSE_TEST_DATA
        payload_data['teacher_id'] = db_subject.teacher_id
        payload_data['subject_id'] = db_subject.id
        response = self.client.post(self.url, json=payload_data)
        response_data = response.get_json()
        expected_result = response_test_course_data.RESPONSE_POST_COURSE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_201_CREATED.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Course).count())

    def test_post_courses_invalid_json_payload(self) -> None:
        """Test POST '/courses' endpoint with invalid empty json payload."""
        response = self.client.post(self.url, json=request_test_course_data.ADD_COURSE_EMPTY_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_course_data.RESPONSE_COURSE_INVALID_PAYLOAD
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Course).count())


class PutCourseTestCase(TestMixin, TestCase):
    """Tests for PUT '/courses/{id}' endpoint."""

    def test_put_course_valid_payload_and_teacher_authenticated(self) -> None:
        """Test PUT '/courses/{id}' endpoint with valid payload and auth cookies."""
        db_course = self.add_course_to_db()
        url = url_for('courses.put_course', id=db_course.id)
        payload_data = request_test_course_data.UPDATE_COURSE_TEST_DATA
        response = self.client.put(url, json=payload_data)
        response_data = response.get_json()
        expected_result = response_test_course_data.RESPONSE_COURSE_UPDATE_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Course).count())

    def test_put_course_updating_other_course_data(self) -> None:
        """Test PUT '/courses/{id}' endpoint updating other's course information."""
        self.add_course_to_db()
        random_db_course = self.add_random_course_to_db()
        url = url_for('courses.put_course', id=random_db_course.id)
        response = self.client.put(url, json=request_test_course_data.UPDATE_COURSE_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_course_data.RESPONSE_COURSE_UNAUTHORIZED_UPDATE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(2, self.db_session.query(Course).count())


class DeleteCourseTestCase(TestMixin, TestCase):
    """Tests for DELETE '/courses/{id}' endpoint."""

    def test_delete_course_teacher_authenticated_and_deleting_own_course(self) -> None:
        """Test DELETE '/courses/{id}' endpoint with valid auth cookies, teacher deleting own course."""
        db_course = self.add_course_to_db()
        url = url_for('courses.delete_course', id=db_course.id)
        self.assertEqual(1, self.db_session.query(Course).count())
        response = self.client.delete(url)
        response_data = response.get_json()
        expected_result = response_test_course_data.RESPONSE_COURSE_DELETE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_204_NO_CONTENT.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Course).count())

    def test_delete_course_deleting_other_course_data(self) -> None:
        """Test DELETE '/courses/{id}' endpoint deleting other's courses information."""
        self.add_course_to_db()
        random_db_course = self.add_random_course_to_db()
        url = url_for('courses.put_course', id=random_db_course.id)
        response = self.client.delete(url)
        response_data = response.get_json()
        expected_result = response_test_course_data.RESPONSE_COURSE_UNAUTHORIZED_DELETE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(2, self.db_session.query(Course).count())
