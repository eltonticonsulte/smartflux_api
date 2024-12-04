# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from logging import getLogger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import func, case
from .connect import DBConnectionHandler
from .schema import User, Device, Zone, EventCounter


class DataBase:
    def __init__(self) -> None:
        self.log = getLogger(__name__)

    def create_device(self, user: User) -> int:
        with DBConnectionHandler() as db:
            try:
                db.__session.add(user)
                db.__session.commit()
                return user.id
            except Exception as exception:
                db.__session.rollback()
                raise exception
