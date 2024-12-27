# -*- coding: utf-8 -*-
import logging
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from .base_repository import BaseRepository
from ..database import Empresa
from ..database import IntegrityError, DBConnectionHandler
from ..dto import EmpresaDTO
from ..mappers import EmpresaMapper


class RepositoryEmpresaExecption(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class EmpresaRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, name: str) -> int:
        self.log.debug(f"create_empresa {name}")
        db_empresa = Empresa(name=name, is_active=True)
        try:
            return self.add(db_empresa)
        except IntegrityError:
            raise RepositoryEmpresaExecption(f"Empresa {name} already exists")
        except Exception as error:
            self.log.critical(error)
            raise error

    def get_all(self) -> List[EmpresaDTO]:
        empresas = super().get_all(Empresa)
        return [EmpresaMapper.to_dto(empresa) for empresa in empresas]

    def get_empresa_by_name(self, name: str) -> Empresa:
        try:
            with DBConnectionHandler() as db:
                empresa = db.query(Empresa).filter(Empresa.name == name).one_or_none()
                return EmpresaMapper.to_dto(empresa)
        except NoResultFound:
            raise RepositoryEmpresaExecption(f'User "{name}" not found')
        except Exception as error:
            db.rollback()
            raise error
