# -*- coding: utf-8 -*-
import unittest
import logging
from fastapi.testclient import TestClient
from unittest.mock import Mock
from fastapi import HTTPException
from src.interfaces import InterfaceAuthService
from src.controllers import auth
from main import app


class MockAuthController(InterfaceAuthService):
    def auth_user(self, username: str, password: str) -> str:

        if username == "testuser" and password == "testpass":
            return "mock_token"
        raise Exception("Invalid credentials")

    def current_user(self, token: str) -> str:
        if token == "mock_token":
            return "testuser"
        raise Exception("Invalid token")


def get_mock_controller_auth():
    return MockAuthController()


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger(__name__)
        app.dependency_overrides[auth.get_service_auth] = get_mock_controller_auth
        self.client = TestClient(app)

    def tearDown(self):
        pass

    def test_successful_login(self):
        response = self.client.post(
            "/api/user/login", data={"username": "testuser", "password": "testpass"}
        )
        self.log.info(response.json())

        # self.mock_get_controller.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"access_token": "mock_token", "token_type": "bearer"}
        )

    def xtest_failed_login(self):
        response = self.client.post(
            "/login",
            data={
                "username": "wronguser",
                "password": "wrongpass",
                "grant_type": "password",
            },
        )

        self.assertEqual(response.status_code, 500)
        self.assertIn("Invalid credentials", response.json()["detail"])

    def xtest_successful_status_check(self):
        response = self.client.get(
            "/status", headers={"Authorization": "Bearer mock_token"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "name": "testuser"})

    def xtest_failed_status_check_invalid_token(self):
        response = self.client.get(
            "/status", headers={"Authorization": "Bearer invalid_token"}
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid token", response.json()["detail"])

    def xtest_missing_auth_header_status_check(self):
        response = self.client.get("/status")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Not authenticated")

    def xtest_login_controller_exception(self):
        self.mock_controller.login = Mock(side_effect=Exception("Database error"))

        response = self.client.post(
            "/login",
            data={
                "username": "testuser",
                "password": "testpass",
                "grant_type": "password",
            },
        )

        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json()["detail"])

    def xtest_status_controller_exception(self):
        self.mock_controller.current_user = Mock(
            side_effect=Exception("Database error")
        )

        response = self.client.get(
            "/status", headers={"Authorization": "Bearer mock_token"}
        )

        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
