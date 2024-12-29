# -*- coding: utf-8 -*-
from abc import ABC
from typing import Generic, List, TypeVar
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import func, case
from ..database.connect import DBConnectionHandler


T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    def create(self, entity: T) -> int:
        pass

    # @abstractmethod
    # def update(self, entity: T) -> int:
    #    raise NotImplementedError("Method not implemented")

    # @abstractmethod
    # def delete(self, entity_id: int) -> None:
    #    raise NotImplementedError("Method not implemented")

    def get_all(self, entity: T) -> List[T]:
        with DBConnectionHandler() as db:
            try:
                return db.query(entity).all()
            except Exception as error:
                db.rollback()
                raise error
