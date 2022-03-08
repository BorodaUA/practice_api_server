from unittest import TestCase

from flask import url_for

from common.constants.http import HttpStatusCodeConstants
from common.tests.generic import TestMixin
from common.tests.test_data.students import request_test_student_data
from courses.models import CourseStudentAssociation
from courses.tests.test_data import response_test_course_students_data


class GetCourseStudentsTestCase(TestMixin, TestCase):
    """Tests for GET '/courses/{id}/students' endpoint."""

    def test_get_course_students_empty_db(self) -> None:
        """Test GET '/courses/{id}/students' endpoint with no student's data added to the course."""
        db_course = self.add_course_to_db()
        url = url_for('courses.course_students.get_course_students', id=db_course.id)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_course_students_data.RESPONSE_COURSE_STUDENTS_EMPTY_DB
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(0, self.db_session.query(CourseStudentAssociation).count())

    def test_get_course_students_test_data_in_db(self) -> None:
        """Test GET '/courses/{id}/students' endpoint with student's test data added to the course."""
        db_course_with_student = self.add_student_to_course()
        url = url_for('courses.course_students.get_course_students', id=db_course_with_student.id)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_course_students_data.response_test_student_data.RESPONSE_GET_STUDENTS
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(CourseStudentAssociation).count())


class GetCourseStudentTestCase(TestMixin, TestCase):
    """Tests for GET '/courses/{id}/students/{id}' endpoint."""

    def test_get_course_student_no_test_data_in_db(self) -> None:
        """Test GET '/courses/{id}/students/{id}' endpoint with no student's test data added to the course."""
        db_course = self.add_course_to_db()
        url = url_for(
            'courses.course_students.get_course_student',
            id=db_course.id,
            student_id=request_test_student_data.DUMMY_STUDENT_UUID,
        )
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_course_students_data.RESPONSE_COURSE_STUDENT_NOT_FOUND
        response_test_course_students_data.RESPONSE_COURSE_STUDENT_NOT_FOUND['errors']['message'] = (
            response_test_course_students_data.RESPONSE_COURSE_STUDENT_NOT_FOUND['errors']['message'].format(
                student_id=request_test_student_data.DUMMY_STUDENT_UUID, course_id=db_course.id,
            )
        )
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_404_NOT_FOUND.value, response.status_code)
        self.assertEqual(0, self.db_session.query(CourseStudentAssociation).count())

    def test_get_course_student_test_data_in_db(self) -> None:
        """Test GET '/courses/{id}/students/{id}' endpoint with student's test data added to the course."""
        db_course_with_student = self.add_student_to_course()
        url = url_for(
            'courses.course_students.get_course_student',
            id=db_course_with_student.id,
            student_id=db_course_with_student.students[0].id,
        )
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_course_students_data.response_test_student_data.RESPONSE_GET_STUDENT
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(CourseStudentAssociation).count())


class PostCourseStudentsTestCase(TestMixin, TestCase):
    """Tests for POST '/courses/{id}/students' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('courses.post_courses')

    def test_post_course_students_valid_payload(self) -> None:
        """Test POST '/courses/{id}/students' endpoint with valid json payload."""
        db_course = self.add_course_to_db()
        db_student = self.add_random_student_to_db()
        payload_data = {}
        payload_data['id'] = db_student.id
        url = url_for('courses.course_students.post_course_students', id=db_course.id)
        response = self.client.post(url, json=payload_data)
        response_data = response.get_json()
        expected_result = response_test_course_students_data.response_test_student_data.RESPONSE_POST_STUDENT
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_201_CREATED.value, response.status_code)
        self.assertEqual(1, self.db_session.query(CourseStudentAssociation).count())

    def test_post_course_students_invalid_json_payload(self) -> None:
        """Test POST '/courses/{id}/students' endpoint with invalid empty json payload."""
        db_course = self.add_course_to_db()
        url = url_for('courses.course_students.post_course_students', id=db_course.id)
        response = self.client.post(url, json=request_test_student_data.ADD_STUDENT_EMPTY_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_course_students_data.RESPONSE_COURSE_STUDENT_INVALID_PAYLOAD
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(0, self.db_session.query(CourseStudentAssociation).count())


class DeleteCourseStudentTestCase(TestMixin, TestCase):
    """Tests for DELETE '/courses/{id}/students/{id}' endpoint."""

    def test_delete_student_from_course_student_authenticated_and_deleting_himself(self) -> None:
        """Test DELETE '/courses/{id}/students/{id}' endpoint with valid auth cookies, student deleting himself."""
        db_course_with_student = self.add_student_to_course()
        url = url_for(
            'courses.course_students.delete_course_student',
            id=db_course_with_student.id,
            student_id=db_course_with_student.students[0].id,
        )
        self.assertEqual(1, self.db_session.query(CourseStudentAssociation).count())
        response = self.client.delete(url)
        response_data = response.get_json()
        expected_result = response_test_course_students_data.RESPONSE_COURSE_STUDENTS_DELETE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(0, self.db_session.query(CourseStudentAssociation).count())

    def test_delete_student_from_course_student_deleting_other_student(self) -> None:
        """Test DELETE '/courses/{id}/students/{id}' endpoint student deleting other student from course."""
        first_db_course_with_student = self.add_random_student_to_course()
        second_db_course_with_student = self.add_student_to_course() # noqa
        url = url_for(
            'courses.course_students.delete_course_student',
            id=first_db_course_with_student.id,
            student_id=first_db_course_with_student.students[0].id,
        )
        self.assertEqual(2, self.db_session.query(CourseStudentAssociation).count())
        response = self.client.delete(url)
        response_data = response.get_json()
        expected_result = response_test_course_students_data.RESPONSE_COURSE_STUDENT_UNAUTHORIZED_DELETE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(2, self.db_session.query(CourseStudentAssociation).count())
