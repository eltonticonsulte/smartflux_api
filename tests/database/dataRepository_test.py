# -*- coding: utf-8 -*-
import unittest
import uuid
from unittest.mock import patch
from src.database import DataRepository, Empresa, DBConnectionHandler
from core import get_settings


def create_data_base():
    engine = DBConnectionHandler.get_engine("sqlite:///:memory:")
    Empresa.metadata.create_all(engine)
    print("Database created")


class TestDataRepositoryEmpresa(unittest.TestCase):
    def setUp(self):
        create_data_base()
        self.repo = DataRepository()
        self.name = "dflaskfddj"

    def tearDown(self) -> None:
        with DBConnectionHandler() as session:
            session.query(Empresa).filter(Empresa.name == self.name).delete()
            session.commit()

    def test_add_success(self):
        empresa = Empresa(name=self.name, password_hash=str(uuid.uuid4()))
        result_id = self.repo.add(empresa)
        self.assertEqual(type(result_id), int)
        print("id", result_id)

    def xtest_add_failure(self):
        with patch("src.database.dataRepository.DBConnectionHandler") as mock_db:
            mock_db.return_value.add.side_effect = Exception("Test Exception")
            mock_db.return_value.commit.return_value = None
            mock_db.return_value.rollback.return_value = None
            with self.assertRaises(Exception):
                self.repo.add(self.entity)
            mock_db.assert_called_once()
            mock_db.return_value.add.assert_called_once_with(self.entity)
            mock_db.return_value.commit.assert_not_called()
            mock_db.return_value.rollback.assert_called_once()


if __name__ == "__main__":
    unittest.main()
