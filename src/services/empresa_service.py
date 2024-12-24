# -*- coding: utf-8 -*-
import logging
from fastapi import HTTPException, status, Depends
from typing import List
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from ..repository import UserRepository, EmpresaRepository
from ..common import UserRole
from ..dto import EmpresaDTO
from ..mappers import EmpresaMapper

auth2_scheme = OAuth2PasswordBearer(tokenUrl="api/empresa/login")


class EmpresaServices:
    def __init__(self, empresa_repository: EmpresaRepository):
        self.empresa_repository = empresa_repository
        self.log = logging.getLogger(__name__)

    def create_empresa(self, name_empresa: str) -> int:
        return self.empresa_repository.create(name_empresa)

    def get_all(self) -> List[EmpresaDTO]:
        datas = self.empresa_repository.get_all()
        result = {"data": [empres.to_dict() for empres in datas]}
        return result

    @staticmethod
    def get_current_user(token: str = Depends(auth2_scheme)):
        return token
