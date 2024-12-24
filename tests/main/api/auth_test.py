# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi.exceptions import RequestValidationError
from src.main.api.user import router


class TestLoginRoute(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(router)

    @patch("src.main.composers.auth_compose.AuthComposerLogin.get_token")
    def test_successful_login(self, mock_get_token):
        mock_get_token.return_value = "test_token"
        response = self.client.post(
            "/login", data={"username": "test_user", "password": "test_password"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"access_token": "test_token", "token_type": "bearer"}
        )


if __name__ == "__main__":
    unittest.main()
