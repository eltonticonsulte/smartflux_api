# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch
from src.common import UserRole
from src.repository import EmpresaRepository, RepositoryEmpresaExecption
from src.database import IntegrityError
from src.dto import EmpresaDTO
from src.database import DBConnectionHandler, Empresa
from src.mappers import EmpresaMapper


class TestEmpresaRepository(unittest.TestCase):
    def setUp(self):
        self.empresa_repository = EmpresaRepository()

    @patch.object(DBConnectionHandler, "__enter__")
    @patch.object(DBConnectionHandler, "__exit__", return_value=1)
    def test_create(self, mock_exit, mock_enter):
        mock_db = mock_enter.return_value = 1
        id_empresa = self.empresa_repository.create("name_test")
        self.assertEqual(id_empresa, 1)

    def test_create_duplicate(self):
        def error_mock(*args, **kwargs):
            statement = "INSERT INTO empresa (username) VALUES (?)"
            params = ["test_usernamex"]
            orig = Exception("Duplicate key error")
            raise IntegrityError(statement, params, orig)

        self.empresa_repository.create = Mock(side_effect=error_mock)
        with self.assertRaises(RepositoryEmpresaExecption):
            self.empresa_repository.create("test_usernamex")


if __name__ == "__main__":
    unittest.main()
