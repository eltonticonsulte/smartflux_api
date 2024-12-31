# -*- coding: utf-8 -*-
import logging
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from ..database import Empresa
from ..database import IntegrityError, DBConnectionHandler


class RepositoryEmpresaExecption(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class EmpresaRepository:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, empresa: Empresa) -> int:
        self.log.debug(f"create_empresa {empresa}")

        with DBConnectionHandler() as session:
            try:
                session.add(empresa)
                session.commit()
                return empresa.empresa_id
            except IntegrityError:
                raise RepositoryEmpresaExecption(f"Empresa {empresa} already exists")
            except Exception as error:
                self.log.critical(error, exc_info=error)
                session.rollback()
                raise error

    def get_all(self) -> List[Empresa]:
        with DBConnectionHandler() as session:
            try:
                empresas = session.query(Empresa).all()
                return empresas
            except Exception as error:
                session.rollback()
                raise error

    def get_by_id(self, empresa_id: int) -> Empresa:
        with DBConnectionHandler() as session:
            try:
                empresa = (
                    session.query(Empresa)
                    .filter(Empresa.empresa_id == empresa_id)
                    .one_or_none()
                )
                return empresa
            except NoResultFound:
                raise RepositoryEmpresaExecption(f'User "{empresa_id}" not found')
            except Exception as error:
                session.rollback()
                raise error

    def get_empresa_by_name(self, name: str) -> Empresa:
        try:
            with DBConnectionHandler() as session:
                empresa = (
                    session.query(Empresa).filter(Empresa.name == name).one_or_none()
                )
                return empresa
        except NoResultFound:
            raise RepositoryEmpresaExecption(f'User "{name}" not found')
        except Exception as error:
            session.rollback()
            raise error

    def update(self, empresa: Empresa) -> None:
        with DBConnectionHandler() as session:
            try:
                session.merge(empresa)
                session.commit()
            except Exception as error:
                session.rollback()
                raise error

    def delete(self, empresa_id: int) -> None:
        with DBConnectionHandler() as session:
            try:
                session.query(Empresa).filter(Empresa.empresa_id == empresa_id).delete()
                session.commit()
            except Exception as error:
                session.rollback()
                raise error
