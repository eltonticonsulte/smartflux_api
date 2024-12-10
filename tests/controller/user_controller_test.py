# -*- coding: utf-8 -*-
import unittest
from fastapi.security import OAuth2PasswordRequestForm
from src.controller.user_controller import UserController


import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import Mock
from src.controller.user_controller import UserController
from src.services.user_service import UserServices

import unittest
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import Mock, patch
from src.controller.user_controller import UserController
from src.services.user_service import UserServices


class TestUserController(unittest.TestCase):
    def setUp(self):
        self.user_services = Mock(spec=UserServices)
        self.user_controller = UserController(self.user_services)
        self.client = TestClient(self.user_controller.router)

    def test_get_login_success(self):
        with patch(
            "src.services.user_service.UserServices.create_access_token",
            return_value="test_token",
        ) as mock_create_access_token:
            self.user_services.auth_user.return_value = True
            response = self.client.post(
                "/auth/login",
                data={"username": "test_user", "password": "test_password"},
            )
            print(response)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(), {"access_token": "test_token", "token_type": "bearer"}
            )
            mock_create_access_token.assert_called_once_with(data={"sub": "test_user"})

    def test_get_login_failure(self):
        self.user_services.auth_user.return_value = False
        with self.assertRaises(HTTPException) as exc_info:
            self.client.post(
                "/auth/login",
                data={"username": "test_user", "password": "test_password"},
            )
        self.assertEqual(exc_info.exception.status_code, 422)
        self.assertEqual(exc_info.exception.detail, "Usuario ou senhna invalida")

    def test_get_login_empty_credentials(self):
        with self.assertRaises(RequestValidationError) as exc_info:
            self.client.post("/auth/login", data={"username": ""})
        # self.assertEqual(exc_info.exception.status_code, 422)
        # self.assertEqual(exc_info.exception.detail, "Usuario ou senhna invalida")
