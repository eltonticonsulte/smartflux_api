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

    def create(self, name: str, filial_id: int) -> bool:
        self.log.debug(f"create_user {name}, {filial_id}")
        zone = ZoneDTO(name=name, filial_id=filial_id)

        return self.repository.create(zone)

    def get_by_name(self, name: str) -> ZoneDTO:
        return self.repository.get_by_name(name)

    def get_all(self) -> List[ZoneDTO]:
        return self.repository.get_all()
