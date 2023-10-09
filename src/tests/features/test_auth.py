from src.tests import get_response_body_from_request
from src.tests.factories.user_factory import UserFactory
from src.tests.unittest_helper import BaseTestCaseWithClient

AUTH_URL = "/auth/login"


class AuthLoginTestCase(BaseTestCaseWithClient):
    def setUp(self):
        super().setUp()
        self.base_url = AUTH_URL
        UserFactory.create(email="admin@gmail.com", username="admin", password="admin")

    def test_login_success(self):
        payload = {
            "username": "admin",
            "password": "admin",
        }

        response, body = get_response_body_from_request(
            self.client,
            self.base_url,
            payload,
            method="post",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body["access_token"])

    def test_login_failed(self):
        payload = {
            "username": "admin1",
            "password": "admin1",
        }

        response, body = get_response_body_from_request(
            self.client,
            self.base_url,
            payload,
            method="post",
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(body["message"], "Wrong username or password")
