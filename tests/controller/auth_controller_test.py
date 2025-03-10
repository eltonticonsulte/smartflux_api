# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

# from src.controllers.user import AuthUserRequest


class TestUserController(unittest.TestCase):
    def setUp(self):
        self.services = Mock()
        # self.user_controller = AuthUserRequest(self.services)

    def xtest_successful_login(self):
        self.services.auth_user.return_value = True
        self.user_controller.login("test_user", "test_password")
        self.services.auth_user.assert_called_once_with("test_user", "test_password")
