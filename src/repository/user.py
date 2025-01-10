# -*- coding: utf-8 -*-
import logging
from sqlalchemy.orm.exc import NoResultFound
from ..database import (
    Usuario,
    DBConnectionHandler,
)


class RepositoryAuthExecption(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UserRepository:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, entity: Usuario) -> int:
        with DBConnectionHandler() as session:
            try:
                session.add(entity)
                session.commit()
                return entity.user_id
            except Exception as error:
                session.rollback()
                raise error

    def get_user_by_name(self, username: str) -> Usuario:
        self.log.debug(f"get_user_by_name {username}")
        with DBConnectionHandler() as session:
            try:
                user = (
                    session.query(Usuario)
                    .filter(Usuario.username == username)
                    .one_or_none()
                )
                return user
            except NoResultFound as error:
                raise RepositoryAuthExecption(f'User "{username}" not found') from error
            except Exception as error:
                session.rollback()
                raise error

    def get_by_id(self, user_id: int) -> Usuario:
        with DBConnectionHandler() as session:
            try:
                user = (
                    session.query(Usuario)
                    .filter(Usuario.user_id == user_id)
                    .one_or_none()
                )
                return user
            except NoResultFound:
                raise RepositoryAuthExecption(f'User "{user_id}" not found')
            except Exception as error:
                session.rollback()
                raise error
