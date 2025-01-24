# -*- coding: utf-8 -*-
import logging
from typing import List
from src.repository import EmpresaRepository
from src.dto import RequestCreateEmpresa, ResponseEmpresa, ResquestUpdateEmpresa
from src.mappers import EmpresaMapper


class EmpresaServices:
    def __init__(self, repository: EmpresaRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, request: RequestCreateEmpresa) -> ResponseEmpresa:
        self.log.debug(f"create_empresa {request}")
        empresa = EmpresaMapper.create_request_to_entity(request)
        new_id = self.repository.create(empresa)
        new_empresa = self.repository.get_by_id(new_id)
        return EmpresaMapper.get_entity_to_response(new_empresa)

    def get_all(self) -> List[ResponseEmpresa]:
        empresas = self.repository.get_all()
        result = [EmpresaMapper.get_entity_to_response(empresa) for empresa in empresas]
        return result

    def get_by_id(self, empresa_id: int) -> ResponseEmpresa:
        empresa = self.repository.get_by_id(empresa_id)
        if empresa is None:
            raise Exception(f"Empresa not found by id {empresa_id}")
        return EmpresaMapper.get_entity_to_response(empresa)

    def update(
        self, empresa_id: int, empresa: ResquestUpdateEmpresa
    ) -> ResponseEmpresa:
        self.log.debug(f"update {empresa}")
        empresa = EmpresaMapper.update_request_to_entity(empresa_id, empresa)
        self.repository.update(empresa)
        empresa_updated = self.repository.get_by_id(empresa_id)
        self.log.debug(f"updated {empresa_updated}")
        return EmpresaMapper.get_entity_to_response(empresa_updated)

    def delete(self, empresa_id: int):
        self.repository.delete(empresa_id)
