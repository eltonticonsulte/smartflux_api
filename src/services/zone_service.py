# -*- coding: utf-8 -*-
import logging
from typing import List
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core import get_settings
from ..repository import ZoneRepository
from ..dto import ZoneDTO
from ..mappers import ZoneMapper


class ZoneServices:
    def __init__(self, repository: ZoneRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, user: ZoneDTO) -> bool:
        data_user: ZoneDTO = self.repository.get_by_name(user.username)
        if data_user.username != "":
            raise ValueError("User name already exists")

        return self.repository.create_user(user)

    def get_by_name(self, name: str) -> ZoneDTO:
        return self.repository.get_by_name(name)

    def get_all(self) -> List[ZoneDTO]:
        return self.repository.get_all()
