# -*- coding: utf-8 -*-

from src.mappers.empresa import EmpresaMapper
from src.database import Empresa
from src.dto import (
    CreateEmpresaRequest,
    GetEmpresaResponse,
    UpdateEmpresaRequest,
)

import unittest
from src.mappers.empresa import EmpresaMapper
from src.dto import UpdateEmpresaRequest
from src.database import Empresa


class TestEmpresaMapper(unittest.TestCase):
    def xtest_update_request_to_entity_with_all_fields(self):
        empresa_id = 1
        empresa_request = UpdateEmpresaRequest(
            name="name", is_active=True, description="description"
        )
        expected_empresa = Empresa(
            empresa_id=empresa_id,
            name="name",
            is_active=True,
            description="description",
        )
        result = EmpresaMapper.update_request_to_entity(empresa_id, empresa_request)
        self.assertEqual(result.empresa_id, expected_empresa.empresa_id)
        self.assertEqual(result.name, expected_empresa.name)
        self.assertEqual(result.is_active, expected_empresa.is_active)
        self.assertEqual(result.description, expected_empresa.description)

    def test_update_request_to_entity_with_none_fields(self):
        empresa_id = 1
        empresa_request = UpdateEmpresaRequest()
        expected_empresa = Empresa(
            empresa_id=empresa_id, name=None, is_active=None, description=None
        )
        result = EmpresaMapper.update_request_to_entity(empresa_id, empresa_request)
        self.assertEqual(result.empresa_id, expected_empresa.empresa_id)
        self.assertEqual(result.name, expected_empresa.name)
        self.assertEqual(result.is_active, expected_empresa.is_active)
        self.assertEqual(result.description, expected_empresa.description)

    def test_update_request_to_entity_with_partial_fields(self):
        empresa_id = 1
        empresa_request = UpdateEmpresaRequest(name="name")
        expected_empresa = Empresa(
            empresa_id=empresa_id, name="name", is_active=None, description=None
        )
        result = EmpresaMapper.update_request_to_entity(empresa_id, empresa_request)
        self.assertEqual(result.empresa_id, expected_empresa.empresa_id)
        self.assertEqual(result.name, expected_empresa.name)
        self.assertEqual(result.is_active, expected_empresa.is_active)
        self.assertEqual(result.description, expected_empresa.description)
