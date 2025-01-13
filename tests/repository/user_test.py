# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch, ANY
from src.enums import UserRule
from src.repository import UserRepository, RepositoryAuthExecption
from src.database import DBConnectionHandler, Usuario


class TestAuthRepository(unittest.TestCase):
    def setUp(self):
        self.auth_repository = UserRepository()

    def test_create(self):
        with patch.object(DBConnectionHandler, "__enter__") as mock_session:
            mock_commit = Mock()
            mock_commit.return_value = 1
            mock_add = Mock()
            mock_session = mock_session.return_value
            mock_session.add = mock_add
            mock_session.commit = mock_commit

            user = Usuario(
                username="test_username",
                password_hash="test_hash_password",
                role=UserRule.ADMIN,
                is_active=True,
            )

            self.auth_repository.create(user)
            mock_add.assert_called_once_with(user)
            mock_commit.assert_called_once_with()

    def test_get_user_by_name_found(self):
        with patch.object(DBConnectionHandler, "__enter__") as mock_session:
            mock_query = Mock()
            mock_filter = Mock()
            Mock()

            mock_session.return_value.query.return_value = mock_query
            mock_query.filter.return_value = mock_filter
            mock_filter.one_or_none.return_value = Usuario(
                username="test_username",
                password_hash="test_hash_password",
                role=UserRule.ADMIN,
                is_active=True,
            )

            user = self.auth_repository.get_user_by_name("test_username")
            mock_session.return_value.query.assert_called_once_with(Usuario)
            mock_query.filter.assert_called_once_with(ANY)
            mock_filter.one_or_none.assert_called_once_with()
            assert user.username == "test_username"
            assert user.role == UserRule.ADMIN


if __name__ == "__main__":
    unittest.main()
