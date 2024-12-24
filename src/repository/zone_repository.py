# -*- coding: utf-8 -*-
import logging
from ..database import (
    Zone,
    DBConnectionHandler,
)
from .base_repository import BaseRepository
from ..dto import UserDTO
from ..common import UserRole
from ..mappers import UserMapper


class UserRepository(BaseRepository):
    def __init__(self):

        self.log = logging.getLogger(__name__)

    def create_user(self, user: UserDTO) -> bool:
        self.log.debug(f"create_user {user}")
        db_user = UserMapper.to_entity(user)
        self.add(db_user)
        return True
