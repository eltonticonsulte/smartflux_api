# -*- coding: utf-8 -*-
import logging
from typing import List
from uuid import UUID
from src.interfaces import InterfaceFilialService
from src.repository import FilialRepository
from src.dto import (
    RequestCreateFilial,
    RequestUpdateFilial,
    ResponseFilial,
)
from src.mappers import FilialMapper
from src.database import Filial


class FilialServices(InterfaceFilialService):
    def __init__(self, repository: FilialRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, resquest: RequestCreateFilial) -> ResponseFilial:
        filial = FilialMapper.create_request_to_entity(resquest)
        filial_id = self.repository.create(filial)
        entity = self.repository.get_by_id(filial_id)
        return FilialMapper.get_entity_to_response(entity)

    def get_all(self) -> List[ResponseFilial]:
        datas: List[Filial] = self.repository.get_all()
        result = [FilialMapper.get_entity_to_response(filial) for filial in datas]
        return result

    def get_by_id(self, filial_id: int) -> ResponseFilial:
        filial = self.repository.get_by_id(filial_id)
        return FilialMapper.get_entity_to_response(filial)

    def get_by_token(self, token: UUID) -> ResponseFilial:
        self.log.debug(f"validate_token {token}")
        filial = self.repository.get_by_token(token)
        if filial is None:
            raise ValueError("Token filial é inválido")
        if not filial.is_active:
            raise ValueError("Filial inativa")
        return FilialMapper.get_entity_to_response(filial)

    def check_token(self, token: UUID) -> None:
        filial = self.repository.get_by_token(token)
        if filial is None:
            raise ValueError("Token filial é inválido code 002")
        if filial.token_api != token:
            raise ValueError("Token filial é inválido code 003")
        if not filial.is_active:
            raise ValueError("Filial inativa")

    def update(self, filial_id: int, request: RequestUpdateFilial) -> ResponseFilial:
        entity = FilialMapper.update_request_to_entity(filial_id, request)
        self.repository.update(entity)
        result = self.repository.get_by_id(filial_id)
        return FilialMapper.get_entity_to_response(result)

    def delete(self, filial_id: int) -> None:
        self.repository.delete(filial_id)
