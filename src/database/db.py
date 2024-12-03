# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import os
from logging import getLogger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import func, case
from .connect import DBConnectionHandler
from .schema import User, Device, Zone, EventCounter


class DataBase:
    def __init__(self, path_db: str = "") -> None:
        self.log = getLogger(__name__)
        self.dir_db_backup = os.path.join("test", "backup_db")
        if not os.path.isdir(self.dir_db_backup):
            os.makedirs(self.dir_db_backup, exist_ok=True)

        self.path_db = path_db
        if self.path_db == "":
            version = os.environ.get("__VERSION__")
            self.path_db = os.path.join(
                "test", f"devices_database_V{version.split('.')[0]}_.db"
            )

        self.log.debug(f"__init__ checking file {self.path_db}")

        if not os.path.isfile(self.path_db):
            self.create_data_base()

    def get_path_db(self):
        return self.path_db

    def create_data_base(self) -> None:
        self.log.info(f"Criando base de dados {self.path_db}")
        with DBConnectionHandler(path_db=self.path_db) as eng:
            User.metadata.create_all(eng.get_engine())
            eng.session.commit()

    def create_device(self, user: User) -> int:
        with DBConnectionHandler(self.path_db) as db:
            try:
                db.session.add(user)
                db.session.commit()
                return user.id
            except Exception as exception:
                db.session.rollback()
                raise exception
