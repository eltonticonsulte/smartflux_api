# -*- coding: utf-8 -*-
import logging
from typing import List
from uuid import UUID
from ..repository import FilialRepository
from ..dto import (
    CreateFilialRequest,
    UpdateFilialRequest,
    GetFilialResponse,
)
from ..mappers import FilialMapper
from ..database import Filial


class FilialServices:
    def __init__(self, repository: FilialRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, resquest: CreateFilialRequest) -> GetFilialResponse:
        filial = FilialMapper.create_request_to_entity(resquest)
        filial_id = self.repository.create(filial)
        entity = self.repository.get_by_id(filial_id)
        return FilialMapper.get_entity_to_response(entity)

    def get_all(self) -> List[GetFilialResponse]:
        datas: List[Filial] = self.repository.get_all()
        result = [FilialMapper.get_entity_to_response(filial) for filial in datas]
        return result

    def get_by_token(self, token: UUID) -> GetFilialResponse:
        self.log.debug(f"validate_token {token}")
        filial = self.repository.get_by_token(token)
        if filial is None:
            raise ValueError("Token filial é inválido")
        if not filial.is_active:
            raise ValueError("Filial inativa")
        return FilialMapper.get_entity_to_response(filial)

    def auth(self, name: str, password: str) -> None:
        filial: Filial = self.repository.get_by_name(name)
        if str(filial.password_hash) != password:
            self.log.error(filial.password_hash, password)
            raise ValueError("Senha inválida")
        if not filial.is_active:
            raise ValueError("Usuário inativo")

    def update(self, filial_id: int, request: UpdateFilialRequest) -> GetFilialResponse:
        entity = FilialMapper.update_request_to_entity(filial_id, request)
        self.repository.update(entity)
        result = self.repository.get_by_id(filial_id)
        return FilialMapper.get_entity_to_response(result)

    def delete(self, id: int) -> None:
        self.repository.delete(id)
