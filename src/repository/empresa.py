# -*- coding: utf-8 -*-
import logging
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from .base_repository import BaseRepository
from ..database import Empresa
from ..database import IntegrityError, DBConnectionHandler
from ..mappers import EmpresaMapper


class RepositoryEmpresaExecption(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class EmpresaRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, empresa: Empresa) -> int:
        self.log.debug(f"create_empresa {empresa}")

        with DBConnectionHandler() as db:
            try:
                db.add(empresa)
                db.commit()
                return empresa.empresa_id
            except IntegrityError:
                raise RepositoryEmpresaExecption(f"Empresa {empresa} already exists")
            except Exception as error:
                self.log.critical(error, exc_info=error)
                db.rollback()
                raise error

    def get_all(self) -> List[Empresa]:
        with DBConnectionHandler() as db:
            try:
                empresas = db.query(Empresa).all()
                return empresas
            except Exception as error:
                db.rollback()
                raise error

    def get_by_id(self, empresa_id: int) -> Empresa:
        with DBConnectionHandler() as db:
            try:
                empresa = (
                    db.query(Empresa)
                    .filter(Empresa.empresa_id == empresa_id)
                    .one_or_none()
                )
                return empresa
            except NoResultFound:
                raise RepositoryEmpresaExecption(f'User "{empresa_id}" not found')
            except Exception as error:
                db.rollback()
                raise error

    def get_empresa_by_name(self, name: str) -> Empresa:
        try:
            with DBConnectionHandler() as db:
                empresa = db.query(Empresa).filter(Empresa.name == name).one_or_none()
                return empresa
        except NoResultFound:
            raise RepositoryEmpresaExecption(f'User "{name}" not found')
        except Exception as error:
            db.rollback()
            raise error
