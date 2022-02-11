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
