# -*- coding: utf-8 -*-
import logging
from typing import List
from ..common import ExceptionUserNameExists
from .base_repository import BaseRepository
from ..database import Empresa, Camera, Zone, EventCountTemp
from ..database import IntegrityError, DBConnectionHandler
from ..dto import EmpresaDTO
from ..mappers import EmpresaMapper


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

    def get_all(self) -> List[EmpresaDTO]:
        try:
            with DBConnectionHandler() as session:
                empresas = session.query(Empresa).all()
                return [EmpresaMapper.to_dto(empresa) for empresa in empresas]
        except Exception as error:
            self.log.critical(error)
            raise error

    def get_empresa_by_name(self, name: str) -> Empresa:
        try:
            with DBConnectionHandler() as session:
                empresa = (
                    session.query(Empresa).filter(Empresa.name == name).one_or_none()
                )
                if empresa is None:
                    raise ValueError("Empresa not found")
                return EmpresaMapper.to_dto(empresa)
        except Exception as error:
            self.log.critical(error)
            raise error
