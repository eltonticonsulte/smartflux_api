# -*- coding: utf-8 -*-
import logging
from uuid import uuid4
from ..common import ExceptionUserNameExists
from .base_repository import BaseRepository
from ..database import Empresa, Camera, Zone, EventCountTemp
from ..database import IntegrityError


class EmpresaRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create_empresa(self, name: str):
        self.log.debug(f"create_empresa {name}")
        db_empresa = Empresa(name=name, is_active=True)
        try:
            self.add(db_empresa)
        except IntegrityError:
            raise ExceptionUserNameExists(name)

    def get_login(self, user) -> Empresa:
        self.log.debug(f"get_login {user}")
        return self.data_base.get_login(user)

    def genetate_token(self):
        return str(uuid4())
