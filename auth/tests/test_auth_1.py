from unittest import TestCase

from flask import url_for

from auth.tests.test_data import response_auth_user_data
from common.constants.http import HttpStatusCodeConstants
from common.tests.generic import TestMixin
from common.tests.test_data.auth import requests_test_auth_data
from users.models import User
from users.tests.test_data import response_test_user_data


class PostAuthLoginTestCase(TestMixin, TestCase):
    """Tests for POST '/auth/login' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('auth.login')

    def test_post_auth_login_with_valid_credentials(self) -> None:
        """Test Post '/auth/login' endpoint with user's data added to the db, and valid credentials."""
        self.add_user_to_db()
        response = self.client.post(self.url, json=requests_test_auth_data.LOGIN_VALID_USER_CREDENTIALS)
        response_data = response.get_json()
        expected_result = response_auth_user_data.RESPONSE_VALID_LOGIN_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(User).count())

    def test_post_auth_login_with_invalid_password(self) -> None:
        """Test Post '/auth/login' endpoint with user's data added to the db, and invalid user's password."""
        self.add_user_to_db()
        response = self.client.post(self.url, json=requests_test_auth_data.LOGIN_INVALID_USER_PASSWORD)
        response_data = response.get_json()
        expected_result = response_auth_user_data.RESPONSE_INVALID_LOGIN_PASSWORD
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_401_UNAUTHORIZED.value, response.status_code)
        self.assertEqual(1, self.db_session.query(User).count())


class GetAuthMeTestCase(TestMixin, TestCase):
    """Tests for POST '/auth/me' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('auth.me')

    def test_get_auth_me_with_no_credentials(self) -> None:
        """Test Post '/auth/me' endpoint with no authorization cookies in the request."""
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = response_auth_user_data.RESPONSE_NO_ACCESS_COOKIES
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_401_UNAUTHORIZED.value, response.status_code)
        self.assertEqual(0, self.db_session.query(User).count())

    def test_get_auth_me_with_valid_credentials(self) -> None:
        """Test Post '/auth/me' endpoint with valid authorization cookies in the request."""
        self.authorize_user()
        response = self.client.get(self.url)
        response_data = response.get_json()
        expected_result = response_test_user_data.RESPONSE_USER_TEST_DATA
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(User).count())


class PostAuthLogoutTestCase(TestMixin, TestCase):
    """Tests for POST '/auth/logout' endpoint."""

    def setUp(self) -> None:
        super().setUp()
        self.url = url_for('auth.logout')

    def test_post_auth_logout_with_no_authorization_cookies(self) -> None:
        """Test Post '/auth/logout' endpoint with no authorization cookies in the request."""
        response = self.client.post(self.url)
        response_data = response.get_json()
        expected_result = response_auth_user_data.RESPONSE_NO_ACCESS_COOKIES
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_401_UNAUTHORIZED.value, response.status_code)
        self.assertEqual(0, self.db_session.query(User).count())

    def test_post_auth_logout_user_signed_id(self) -> None:
        """Test Post '/auth/logout' endpoint with valid authorization cookies in the request."""
        self.authorize_user()
        response = self.client.post(self.url)
        response_data = response.get_json()
        expected_result = response_auth_user_data.RESPONSE_USER_LOGOUT_MSG
        self.assertEqual(expected_result, response_data)
        self.assertEqual(HttpStatusCodeConstants.HTTP_200_OK.value, response.status_code)
        self.assertEqual(1, self.db_session.query(User).count())
