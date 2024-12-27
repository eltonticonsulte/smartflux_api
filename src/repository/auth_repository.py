# -*- coding: utf-8 -*-
import logging
from typing import Optional
from sqlalchemy.orm.exc import NoResultFound
from ..database import (
    Usuario,
    DBConnectionHandler,
)
from .base_repository import BaseRepository
from ..dto import UserDTO
from ..mappers import UserMapper


class RepositoryAuthExecption(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class AuthRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def get_user_by_name(self, username: str) -> Optional[UserDTO]:
        self.log.debug(f"get_user_by_name {username}")
        with DBConnectionHandler() as db:
            try:
                user = (
                    db.query(Usuario).filter(Usuario.username == username).one_or_none()
                )
                return UserMapper.to_dto(user)
            except NoResultFound:
                raise RepositoryAuthExecption(f'User "{username}" not found')
            except Exception as error:
                db.rollback()
                raise error
