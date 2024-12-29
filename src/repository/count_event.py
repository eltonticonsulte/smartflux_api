# -*- coding: utf-8 -*-
from typing import List
from ..database import DBConnectionHandler, EventCountTemp
from .base_repository import BaseRepository


class RepositoryCountEventException(Exception):
    def __init__(self, message):
        super().__init__(message)


class CountEventRepository(BaseRepository):
    def __init__(self):
        pass

    def add_all(self, events: List[EventCountTemp]):
        with DBConnectionHandler() as db:
            try:
                db.bulk_save_objects(events)
                db.commit()
            except Exception as error:
                db.rollback()
                raise error
