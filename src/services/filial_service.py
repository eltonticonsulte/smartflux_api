# -*- coding: utf-8 -*-
import logging
from fastapi import HTTPException, status, Depends
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from core import get_settings
from ..repository import FilialRepository
from ..dto import FilialDTO
from ..mappers import FilialMapper

auth2_scheme = OAuth2PasswordBearer(tokenUrl="api/filial/login")


class FilialServices:
    def __init__(self, filial_repository: FilialRepository):
        self.filial_repository = filial_repository
        self.log = logging.getLogger(__name__)

    def create(self, name_empresa: str, cnpj: str, empresa_id: int) -> int:
        dto = FilialDTO(name=name_empresa, cnpj=cnpj, empresa_id=empresa_id)
        return self.filial_repository.create(dto)

    def get_all(self) -> List[FilialDTO]:
        datas = self.filial_repository.get_all()
        result = {"data": [filial.to_dict() for filial in datas]}
        return result

    def auth(self, name: str, password: str) -> bool:
        filial: FilialDTO = self.filial_repository.get_user_by_name(name)
        if filial.password_hash != password:
            return False
        if not filial.is_active:
            return False
        return True

    @staticmethod
    def get_current_user(token: str = Depends(auth2_scheme)):
        return token
