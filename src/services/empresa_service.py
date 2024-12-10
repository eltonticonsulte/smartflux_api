# -*- coding: utf-8 -*-
import logging
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from core import get_settings
from ..database import DBConnectionHandler
from ..repository import UserRepository, EmpresaRepository
from ..common import UserRole
from ..dto import UserDTO
from ..mappers import UserMapper

auth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


class EmpresaServices:
    def __init__(self, empresa_repository: EmpresaRepository):
        self.empresa_repository = empresa_repository
        self.log = logging.getLogger(__name__)

    def create_empresa(self, name_empresa: str) -> int:
        return self.empresa_repository.create_empresa(name_empresa)
