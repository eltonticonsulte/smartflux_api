# -*- coding: utf-8 -*-
import logging
from typing import List
from ..repository import EmpresaRepository
from ..dto import (
    CreateEmpresaRequest,
    CreateEmpresaResponse,
    GetEmpresaResponse,
)
from ..mappers import EmpresaMapper


class EmpresaServices:
    def __init__(self, repository: EmpresaRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, request: CreateEmpresaRequest) -> CreateEmpresaResponse:
        empresa = EmpresaMapper.create_request_to_entity(request)
        new_id = self.repository.create(empresa)
        return CreateEmpresaResponse(empresa_id=new_id, name=request.name)

    def get_all(self) -> List[GetEmpresaResponse]:
        empresas = self.repository.get_all()
        result = [EmpresaMapper.get_entity_to_response(empresa) for empresa in empresas]
        return result

    def get_by_id(self, id: int) -> GetEmpresaResponse:
        empresa = self.repository.get_by_id(id)
        return EmpresaMapper.get_entity_to_response(empresa)

    def update(self, id: int, empresa: CreateEmpresaRequest) -> GetEmpresaResponse:
        self.log.debug(f"update {empresa}")
        empresa = EmpresaMapper.update_request_to_entity(id, empresa)
        self.repository.update(empresa)
        empresa_updated = self.repository.get_by_id(id)
        self.log.debug(f"updated {empresa_updated}")
        return EmpresaMapper.get_entity_to_response(empresa_updated)
