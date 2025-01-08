# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch
from src.enums import UserRole
from src.repository import UserRepository, RepositoryAuthExecption
from src.database import DBConnectionHandler, Usuario


class TestAuthRepository(unittest.TestCase):
    def setUp(self):
        self.auth_repository = UserRepository()

    def xtest_get_user_by_name_found(self):
        user = Usuario(
            username="test_username",
            password_hash="test_hash_password",
            role=UserRole.ADMIN,
            is_active=True,
        )

        self.auth_repository.get_by_name = Mock()
        self.auth_repository.get_by_name.return_value = user

        self.auth_repository.get_user_by_name("test_username")
        # self.assertIsInstance(user_dto, UserDTO)

    @patch.object(DBConnectionHandler, "__enter__")
    @patch.object(DBConnectionHandler, "__exit__", return_value=None)
    def xtest_get_user_by_name_not_found(self, mock_exit, mock_enter):
        mock_db = mock_enter.return_value
        mock_db.query.return_value.filter.return_value.one_or_none.return_value = None
        with self.assertRaises(RepositoryAuthExecption):
            self.auth_repository.get_user_by_name("test_usernamex")


if __name__ == "__main__":
    unittest.main()
