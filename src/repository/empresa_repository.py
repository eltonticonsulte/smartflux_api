# -*- coding: utf-8 -*-
import logging
from uuid import uuid4
from .base_repository import BaseRepository
from ..database import Filial, Camera, Zone, EventCountTemp
from ..database import IntegrityError


class ExceptionUserNameExists(Exception):
    def __init__(self, username: str):
        self.messge = f"User name '{username}' already exists"
        super().__init__(self.messge)

    def __str__(self):
        return self.messge


class EmpresaRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create_empresa(self, user):
        self.log.debug(f"create_user {user}")
        entity_filial = Filial(
            name=user.username,
            description=user.description,
            token_api=self.genetate_token(),
            password_hash=user.password,
        )
        try:
            self.add(entity_filial)
        except IntegrityError:
            raise ExceptionUserNameExists(user.username)

    def get_login(self, user) -> Filial:
        self.log.debug(f"get_login {user}")
        return self.data_base.get_login(user)

    def genetate_token(self):
        return str(uuid4())
