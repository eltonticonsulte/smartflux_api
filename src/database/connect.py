# -*- coding: utf-8 -*-
from logging import getLogger
from typing import Optional, Type, Any
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from core import get_settings


class DBConnectionHandler:
    log = getLogger(__name__)
    __engine = create_engine(
        get_settings().DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=3600,
    )
    __SessionLocal = sessionmaker(bind=__engine)

    def __init__(self) -> None:
        self.session: Optional[Session] = None

    @staticmethod
    def get_engine(cls) -> Engine:
        return cls.__engine

    def __enter__(self) -> Session:
        self.session = self.__SessionLocal()
        return self.session

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> None:
        if self.session:
            if exc_type is not None:
                try:
                    self.session.rollback()
                except SQLAlchemyError as error:
                    self.log.error("error rollback session", exc_info=error)
            try:
                self.session.close()
            except SQLAlchemyError as error:
                self.log.error("error close session", exc_info=error)
            finally:
                self.session = None
