# -*- coding: utf-8 -*-
import logging
from typing import List
from uuid import UUID
from ..repository import FilialRepository
from ..dto import CreateFilialRequest, CreateFilialResponse
from ..mappers import FilialMapper
from ..database import Filial


class FilialServices:
    def __init__(self, repository: FilialRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, resquest: CreateFilialRequest) -> int:
        filial = FilialMapper.create_request_to_entity(resquest)
        filial_id = self.repository.create(filial)
        return CreateFilialResponse(filial_id=filial_id, name_filial=filial.name)

    def get_all(self) -> List[CreateFilialResponse]:
        datas: List[Filial] = self.repository.get_all()
        result = [FilialMapper.get_entity_to_response(filial) for filial in datas]
        return result

    def validate_token(self, token: UUID):
        self.log.debug(f"validate_token {token}")
        filial = self.repository.get_by_token(token)
        if filial is None:
            raise ValueError("Token filial é inválido")

    def auth(self, name: str, password: str) -> None:
        filial: Filial = self.repository.get_by_name(name)
        if str(filial.password_hash) != password:
            self.log.error(filial.password_hash, password)
            raise ValueError("Senha inválida")
        if not filial.is_active:
            raise ValueError("Usuário inativo")
