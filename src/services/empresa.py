# -*- coding: utf-8 -*-
import logging
from fastapi import status, Depends
from typing import List
from ..repository import EmpresaRepository
from ..common import UserRole
from ..dto import (
    CreateEmpresaRequest,
    CreateEmpresaResponse,
    GetEmpresaResponse,
)
from ..mappers import EmpresaMapper


class EmpresaServices:
    def __init__(self, empresa_repository: EmpresaRepository):
        self.empresa_repository = empresa_repository
        self.log = logging.getLogger(__name__)

    def create(self, request: CreateEmpresaRequest) -> CreateEmpresaResponse:
        empresa = EmpresaMapper.create_request_to_entity(request)
        new_id = self.empresa_repository.create(empresa)
        return CreateEmpresaResponse(empresa_id=new_id, name=request.name)

    def get_all(self) -> List[GetEmpresaResponse]:
        empresas = self.empresa_repository.get_all()
        result = [EmpresaMapper.get_entity_to_response(empresa) for empresa in empresas]
        return result
