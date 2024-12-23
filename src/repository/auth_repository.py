# -*- coding: utf-8 -*-
import logging
from typing import Optional
from ..database import (
    Usuario,
    DBConnectionHandler,
)
from .base_repository import BaseRepository
from ..dto import UserDTO
from ..common import UserRole
from ..mappers import UserMapper


class AuthRepository(BaseRepository):
    def __init__(self):

        self.log = logging.getLogger(__name__)

    def get_user_by_name(self, username: str) -> Optional[UserDTO]:
        with DBConnectionHandler() as db:
            try:
                user = (
                    db.query(Usuario).filter(Usuario.username == username).one_or_none()
                )
                if user is None:
                    return UserDTO(
                        username="",
                        password="",
                        hash_password="",
                        role=UserRole.FILIAL,
                        is_active=False,
                    )
                return UserMapper.to_dto(user)
            except Exception as error:
                db.rollback()
                self.log.critical(error)
                raise error
