# -*- coding: utf-8 -*-
import logging
from typing import List
from fastapi.security import OAuth2PasswordBearer
from ..repository import FilialRepository
from ..dto import FilialDTO


auth2_scheme = OAuth2PasswordBearer(tokenUrl="api/filial/login")


class FilialServices:
    def __init__(self, repository: FilialRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, name_empresa: str, cnpj: str, empresa_id: int) -> int:
        dto = FilialDTO(name=name_empresa, cnpj=cnpj, empresa_id=empresa_id)
        return self.repository.create(dto)

    def get_all(self) -> List[FilialDTO]:
        datas = self.repository.get_all()
        result = {"data": [filial.to_dict() for filial in datas]}
        return result

    def auth(self, name: str, password: str) -> None:
        filial: FilialDTO = self.repository.get_by_name(name)
        if str(filial.password_hash) != password:
            self.log.error(filial.password_hash, password)
            raise ValueError("Senha inválida")
        if not filial.is_active:
            raise ValueError("Usuário inativo")
