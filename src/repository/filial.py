# -*- coding: utf-8 -*-
import logging
from uuid import UUID
from typing import List

from ..database import Filial, DBConnectionHandler, IntegrityError


class RepositoryFilialExecption(Exception):
    def __init__(self, message):
        super().__init__(message)


class FilialRepository:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, filial: Filial) -> int:
        with DBConnectionHandler() as session:
            try:
                session.add(filial)
                session.commit()
                return filial.filial_id
            except IntegrityError:
                raise RepositoryFilialExecption(f"Filial {filial.name} already exists")
            except Exception as error:
                self.log.critical(error)
                raise error

    def get_all(self) -> List[Filial]:
        with DBConnectionHandler() as session:
            filials = session.query(Filial).all()
            return filials

    def get_by_token(self, token: UUID) -> Filial:
        with DBConnectionHandler() as session:
            filial = (
                session.query(Filial).filter(Filial.token_api == token).one_or_none()
            )
            return filial

    def get_by_name(self, name: str) -> Filial:
        with DBConnectionHandler() as session:
            filial = session.query(Filial).filter(Filial.name == name).one_or_none()
            if filial is None:
                raise RepositoryFilialExecption(f"Filial {name} not found")
        return filial

    def get_by_id(self, filial_id: int) -> Filial:
        with DBConnectionHandler() as session:
            filial = (
                session.query(Filial)
                .filter(Filial.filial_id == filial_id)
                .one_or_none()
            )
            if filial is None:
                raise RepositoryFilialExecption(f"Filial {filial_id} not found")
        return filial

    def update(self, filial: Filial) -> None:
        with DBConnectionHandler() as session:
            try:
                session.merge(filial)
                session.commit()
            except Exception as error:
                session.rollback()
                raise error

    def delete(self, filial_id: int) -> None:
        with DBConnectionHandler() as session:
            try:
                session.query(Filial).filter(Filial.filial_id == filial_id).delete()
                session.commit()
            except Exception as error:
                session.rollback()
                raise error
