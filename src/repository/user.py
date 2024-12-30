# -*- coding: utf-8 -*-
import logging
from sqlalchemy.orm.exc import NoResultFound
from ..database import (
    Usuario,
    DBConnectionHandler,
)
from .base_repository import BaseRepository

from ..mappers import UserMapper


class RepositoryAuthExecption(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UserRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, entity: Usuario) -> int:
        with DBConnectionHandler() as db:
            try:
                db.add(entity)
                db.commit()
                return entity.id
            except Exception as error:
                db.rollback()
                raise error

    def get_user_by_name(self, username: str) -> Usuario:
        self.log.debug(f"get_user_by_name {username}")
        with DBConnectionHandler() as db:
            try:
                user = (
                    db.query(Usuario).filter(Usuario.username == username).one_or_none()
                )
                return user
            except NoResultFound:
                raise RepositoryAuthExecption(f'User "{username}" not found')
            except Exception as error:
                db.rollback()
                raise error

    def get_by_id(self, user_id: int) -> Usuario:
        with DBConnectionHandler() as db:
            try:
                user = db.query(Usuario).filter(Usuario.id == user_id).one_or_none()
                return user
            except NoResultFound:
                raise RepositoryAuthExecption(f'User "{user_id}" not found')
            except Exception as error:
                db.rollback()
                raise error
