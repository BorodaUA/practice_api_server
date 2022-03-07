from unittest import TestCase

from flask import url_for

from common.constants.http import HttpStatusCodeConstants
from common.tests.generic import TestMixin
from common.tests.test_data.subjects import request_test_subject_data
from subjects.models import Subject
from subjects.tests.test_data import response_test_subject_data


class GetSubjectsTestCase(TestMixin, TestCase):
    """Tests for GET '/subjects' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('subjects.get_subjects')

    def test_get_subjects_empty_db(self) -> None:
        """Test GET '/subjects' endpoint with no subject's data added to the db."""
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = response_test_subject_data.RESPONSE_SUBJECT_EMPTY_DB
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Subject).count())

    def test_get_subjects_test_data_in_db(self) -> None:
        """Test GET '/subjects' endpoint with subject's test data added to the db."""
        self.add_subject_to_db()
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = response_test_subject_data.RESPONSE_GET_SUBJECTS
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Subject).count())


class GetSubjectTestCase(TestMixin, TestCase):
    """Tests for GET '/subjects/{id}' endpoint."""

    def test_get_subject_no_test_data_in_db(self) -> None:
        """Test GET '/subject/{id}' endpoint with no subject's test data added to the db."""
        url = url_for('subjects.get_subject', id=request_test_subject_data.DUMMY_SUBJECT_UUID)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_subject_data.RESPONSE_SUBJECT_NOT_FOUND
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_404_NOT_FOUND.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Subject).count())

    def test_get_subject_test_data_in_db(self) -> None:
        """Test GET '/subjects/{id}' endpoint with subject's test data added to the db."""
        db_subject = self.add_subject_to_db()
        url = url_for('subjects.get_subject', id=db_subject.id)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_subject_data.RESPONSE_GET_SUBJECT
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Subject).count())


class PostSubjectsTestCase(TestMixin, TestCase):
    """Tests for POST '/subjects' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('subjects.post_subject')

    def test_post_subjects_valid_payload(self) -> None:
        """Test POST '/subjects' endpoint with valid json payload."""
        db_teacher = self.add_teacher_to_db()
        payload_data = request_test_subject_data.ADD_SUBJECT_TEST_DATA
        payload_data['teacher_id'] = db_teacher.id
        response = self.client.post(self.url, json=payload_data)
        response_data = response.get_json()
        expected_result = response_test_subject_data.RESPONSE_POST_SUBJECT
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_201_CREATED.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Subject).count())

    def test_post_subjects_invalid_json_payload(self) -> None:
        """Test POST '/subjects' endpoint with invalid empty json payload."""
        response = self.client.post(self.url, json=request_test_subject_data.ADD_SUBJECT_EMPTY_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_subject_data.RESPONSE_SUBJECT_INVALID_PAYLOAD
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Subject).count())


class PutSubjectTestCase(TestMixin, TestCase):
    """Tests for PUT '/subjects/{id}' endpoint."""

    def test_put_subject_valid_payload_and_teacher_authenticated(self) -> None:
        """Test PUT '/subject/{id}' endpoint with valid payload and auth cookies."""
        db_subject = self.add_subject_to_db()
        url = url_for('subjects.put_subject', id=db_subject.id)
        response = self.client.put(url, json=request_test_subject_data.UPDATE_SUBJECT_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_subject_data.RESPONSE_SUBJECT_UPDATE_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(Subject).count())

    def test_put_subject_updating_other_subject_data(self) -> None:
        """Test PUT '/subjects/{id}' endpoint updating other's subject information."""
        self.add_subject_to_db()
        random_db_subject = self.add_random_subject_to_db()
        url = url_for('subjects.put_subject', id=random_db_subject.id)
        response = self.client.put(url, json=request_test_subject_data.UPDATE_SUBJECT_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_subject_data.RESPONSE_SUBJECT_UNAUTHORIZED_UPDATE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(2, self.db_session.query(Subject).count())


class DeleteSubjectTestCase(TestMixin, TestCase):
    """Tests for DELETE '/subjects/{id}' endpoint."""

    def test_delete_subject_teacher_authenticated_and_deleting_own_subject(self) -> None:
        """Test DELETE '/subjects/{id}' endpoint with valid auth cookies, teacher deleting own subject."""
        db_subject = self.add_subject_to_db()
        url = url_for('subjects.delete_subject', id=db_subject.id)
        self.assertEqual(1, self.db_session.query(Subject).count())
        response = self.client.delete(url)
        response_data = response.get_json()
        expected_result = response_test_subject_data.RESPONSE_SUBJECT_DELETE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_204_NO_CONTENT.value, response.status_code)
        self.assertEqual(0, self.db_session.query(Subject).count())

    def test_delete_subject_deleting_other_subject_data(self) -> None:
        """Test DELETE '/subjects/{id}' endpoint deleting other's subject information."""
        self.add_subject_to_db()
        random_db_subject = self.add_random_subject_to_db()
        url = url_for('subjects.put_subject', id=random_db_subject.id)
        response = self.client.delete(url)
        response_data = response.get_json()
        expected_result = response_test_subject_data.RESPONSE_SUBJECT_UNAUTHORIZED_DELETE
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(2, self.db_session.query(Subject).count())
