# -*- coding: utf-8 -*-
import logging
from uuid import uuid4
from ..entity import UserReciver
from ..database import DataBase, User, Device, Zone, EventCounter


class userRepository:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.data_base = DataBase()

    def create_user(self, user: UserReciver):
        self.log.debug(f"create_user {user}")
        db_user = User(
            name=user.username,
            description=user.description,
            token_api=self.genetate_token(),
            password_hash=user.password,
        )
        self.data_base.create_device(db_user)

    def genetate_token(self):
        return str(uuid4())
