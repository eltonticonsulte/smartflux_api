# -*- coding: utf-8 -*-
from logging import getLogger
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Optional
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import func, case
from ..database.connect import DBConnectionHandler
from ..database.schema import (
    Filial,
    Camera,
    Zone,
    EventCountTemp,
    Empresa,
    EventCountHourly,
    Usuario,
)

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> int:
        pass

    @abstractmethod
    def update(self, entity: T) -> int:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        pass


class BaseRepository(Repository[T]):
    def __init__(self):
        self.log = getLogger(__name__)

    def add(self, entity: T) -> int:
        with DBConnectionHandler() as db:
            try:
                db.add(entity)
                db.commit()
                return entity.id
            except Exception as error:
                db.rollback()
                raise error

    def update(self, entity: T) -> int:
        with DBConnectionHandler() as db:
            try:
                db.merge(entity)
                db.commit()
                return entity.id
            except Exception as error:
                db.rollback()
                raise error

    def get_all(self, entity: T) -> List[T]:
        with DBConnectionHandler() as db:
            try:
                return db.query(entity).all()
            except Exception as error:
                db.rollback()
                raise error

    def get_by_name(self, entity: T, name: str) -> Optional[T]:
        with DBConnectionHandler() as db:
            try:
                return db.query(entity).filter(T.name == name).one_or_none()
            except NoResultFound:
                return None
            except Exception as error:
                db.rollback()
                raise error

    def get_by_id(self, entity: T) -> Optional[T]:
        with DBConnectionHandler() as db:
            try:
                return db.query(entity).filter(T.id == entity.entity_id).one_or_none()
            except NoResultFound:
                return None
            except Exception as error:
                db.rollback()
                raise error

    def delete(self, entity: T) -> None:
        with DBConnectionHandler() as db:
            try:
                db.query(entity).filter(T.id == entity.entity_id).delete()
                db.commit()
            except Exception as error:
                db.rollback()
                raise error


class DataRepositoryOtimazeInsert:
    def add(self, events: List[T]) -> int:
        with DBConnectionHandler() as db:
            try:
                db.bulk_save_objects(events)
                db.commit()
            except Exception as error:
                db.rollback()
                raise error
