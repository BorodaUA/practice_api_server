from unittest import TestCase

from flask import url_for

from common.constants.http import HttpStatusCodeConstants
from common.tests.generic import TestMixin
from common.tests.test_data.users import request_test_user_data
from users.models import User
from users.tests.test_data import response_test_user_data


class GetUsersTestCase(TestMixin, TestCase):
    """Tests for GET '/users' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('users.get_users')

    def test_get_users_empty_db(self) -> None:
        """Test GET '/users' endpoint with no user's data added to the db."""
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = []
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(0, self.db_session.query(User).count())

    def test_get_users_test_data_in_db(self) -> None:
        """Test GET '/users' endpoint with user's test data added to the db."""
        self.add_user_to_db()
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = response_test_user_data.RESPONSE_USERS_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(User).count())


class GetUserTestCase(TestMixin, TestCase):
    """Tests for GET '/users/{id}' endpoint."""

    def setUp(self) -> None:
        super().setUp()

    def test_get_user_no_test_data_in_db(self) -> None:
        """Test GET '/users/{id}' endpoint with no user's test data added to the db."""
        url = url_for('users.get_user', id=request_test_user_data.DUMMY_USER_UUID)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_user_data.RESPONSE_USER_NOT_FOUND
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_404_NOT_FOUND.value, response.status_code)
        self.assertEqual(0, self.db_session.query(User).count())

    def test_get_user_test_data_in_db(self) -> None:
        """Test GET '/users/{id}' endpoint with user's test data added to the db."""
        db_user = self.add_user_to_db()
        url = url_for('users.get_user', id=db_user.id)
        response = self.client.get(url)
        response_data = response.get_json()
        expected_result = response_test_user_data.RESPONSE_USER_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(User).count())


class PostUsersTestCase(TestMixin, TestCase):
    """Tests for POST '/users' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('users.get_users')

    def test_post_users_valid_payload(self) -> None:
        """Test POST '/users' endpoint with valid payload and no user's data added to the db."""
        response = self.client.post(self.url, json=request_test_user_data.ADD_USER_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_user_data.RESPONSE_USER_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_201_CREATED.value, response.status_code)
        self.assertEqual(1, self.db_session.query(User).count())

    def test_post_users_invalid_json_payload(self) -> None:
        """Test POST '/users' endpoint with invalid empty json payload."""
        response = self.client.post(self.url, json=request_test_user_data.ADD_USER_EMPTY_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_user_data.RESPONSE_USER_INVALID_PAYLOAD
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(0, self.db_session.query(User).count())

    def test_post_users_duplicate_username(self) -> None:
        """Test POST '/users' endpoint with payload user's username already in the db."""
        self.add_user_to_db()
        response = self.client.post(self.url, json=request_test_user_data.ADD_USER_TEST_DATA)
        response_data = response.get_json()
        expected_result = response_test_user_data.RESPONSE_USER_DUPLICATE_USERNAME
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_400_BAD_REQUEST.value, response.status_code)
        self.assertEqual(1, self.db_session.query(User).count())
