# -*- coding: utf-8 -*-
import logging
from fastapi import status, Depends
from typing import List
from ..repository import EmpresaRepository
from ..common import UserRole
from ..dto import (
    CreateRequestEmpresa,
    CreateResponseEmpresa,
    GetResponseEmpresa,
)
from ..mappers import EmpresaMapper


class EmpresaServices:
    def __init__(self, empresa_repository: EmpresaRepository):
        self.empresa_repository = empresa_repository
        self.log = logging.getLogger(__name__)

    def create(self, request: CreateRequestEmpresa) -> CreateResponseEmpresa:
        empresa = EmpresaMapper.create_request_to_entity(request)
        new_id = self.empresa_repository.create(empresa)
        return CreateResponseEmpresa(empresa_id=new_id)

    def get_all(self) -> List[GetResponseEmpresa]:
        empresas = self.empresa_repository.get_all()
        result = [EmpresaMapper.get_entity_to_response(empresa) for empresa in empresas]
        return result
