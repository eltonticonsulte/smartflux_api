# -*- coding: utf-8 -*-
import logging
from typing import Optional
from ..database import (
    DataUserDB,
    Filial,
    Camera,
    Zone,
    EventCountTemp,
    Usuario,
    DBConnectionHandler,
)
from ..database import IntegrityError
from ..dto import UserDTO
from ..mappers import UserMapper


class ExceptionUserNameExists(Exception):
    def __init__(self, username: str):
        self.messge = f"User name '{username}' already exists"
        super().__init__(self.messge)

    def __str__(self):
        return self.messge


class UserRepository:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.data_base = DataUserDB()

    def get_login(self, user: str) -> Filial:
        self.log.debug(f"get_login {user}")
        user = self.data_base.get_user_by_name(user)
        return user

    def create_user(self, user: UserDTO) -> bool:
        self.log.debug(f"create_user {user}")
        db_user = UserMapper.to_entity(user)
        try:
            with DBConnectionHandler() as session:
                session.add(db_user)
                session.commit()
                return True
        except Exception:
            session.rollback()
            raise ExceptionUserNameExists(user.username)

    def get_user_by_name(self, username: str) -> Optional[UserDTO]:
        with DBConnectionHandler() as db:
            try:
                user = db.query(Usuario).filter(Usuario.name == username).one_or_none()
                return UserMapper.to_dto(user)
            except Exception as error:
                db.rollback()
                raise error
