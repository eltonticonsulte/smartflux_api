# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch
from src.common import UserRole
from src.repository import AuthRepository, RepositoryAuthExecption
from src.dto import UserDTO
from src.database import DBConnectionHandler, Usuario
from src.mappers import UserMapper


class TestAuthRepository(unittest.TestCase):
    def setUp(self):
        self.auth_repository = AuthRepository()

    def test_get_user_by_name_found(self):
        user = Usuario(
            username="test_username",
            password_hash="test_hash_password",
            role=UserRole.ADMIN,
            is_active=True,
        )

        self.auth_repository.get_by_name = Mock()
        self.auth_repository.get_by_name.return_value = user

        user_dto = self.auth_repository.get_user_by_name("test_username")
        self.assertIsInstance(user_dto, UserDTO)

    @patch.object(DBConnectionHandler, "__enter__")
    @patch.object(DBConnectionHandler, "__exit__", return_value=None)
    def stest_get_user_by_name_not_found(self, mock_exit, mock_enter):
        mock_db = mock_enter.return_value
        mock_db.query.return_value.filter.return_value.one_or_none.return_value = None
        with self.assertRaises(RepositoryAuthExecption):
            self.auth_repository.get_user_by_name("test_usernamex")


if __name__ == "__main__":
    unittest.main()
