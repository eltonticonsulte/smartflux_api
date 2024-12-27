# -*- coding: utf-8 -*-
import logging
from typing import Optional
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
        user = self.get_by_name(Usuario, username)
        if user is None:
            raise RepositoryAuthExecption(f'User "{username}" not found')
        return UserMapper.to_dto(user)
