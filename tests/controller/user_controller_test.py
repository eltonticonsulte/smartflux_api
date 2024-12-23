# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi.exceptions import RequestValidationError, HTTPException
from src.controller import AuthController
from src.services import AuthServices


class TestUserController(unittest.TestCase):
    def setUp(self):
        self.services = Mock(spec=AuthServices)
        self.user_controller = AuthController(self.services)
        self.client = TestClient(base_url="api")

    def test_get_login_success(self):
        with patch(
            "src.services.user_service.UserServices.create_access_token",
            return_value="test_token",
        ) as mock_create_access_token:
            self.services.auth_user.return_value = True
            response = self.client.post(
                "/user/login",
                data={"username": "test_user", "password": "test_password"},
            )
            print(response)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(), {"access_token": "test_token", "token_type": "bearer"}
            )
            mock_create_access_token.assert_called_once_with(data={"sub": "test_user"})

    def xtest_get_login_failure(self):
        self.services.auth_user.return_value = False
        with self.assertRaises(HTTPException) as exc_info:
            self.client.post(
                "/user/login",
                data={"username": "test_user", "password": "test_password"},
            )
        self.assertEqual(exc_info.exception.status_code, 422)
        self.assertEqual(exc_info.exception.detail, "Usuario ou senhna invalida")

    def xtest_get_login_empty_credentials(self):
        with self.assertRaises(RequestValidationError) as exc_info:
            self.client.post("/user/login", data={"username": ""})
