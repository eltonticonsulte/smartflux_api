# -*- coding: utf-8 -*-
import logging
from ..common import ExceptionUserNameExists
from .base_repository import BaseRepository
from ..database import Empresa, Camera, Zone, EventCountTemp
from ..database import IntegrityError


class EmpresaRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create_empresa(self, name: str) -> int:
        self.log.debug(f"create_empresa {name}")
        db_empresa = Empresa(name=name, is_active=True)
        try:
            return self.add(db_empresa)
        except IntegrityError:
            raise ExceptionUserNameExists(name)
        except Exception as error:
            self.log.critical(error)
            raise error

    def get_login(self, user) -> Empresa:
        self.log.debug(f"get_login {user}")
        return self.data_base.get_login(user)
