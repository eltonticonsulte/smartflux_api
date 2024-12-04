# -*- coding: utf-8 -*-
from typing import Optional, Type, Any
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from core import get_settings
from contextlib import contextmanager


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__engine = create_engine(
            get_settings().DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=3600,
        )
        self.__session: Optional[Session] = None

    def get_engine(self) -> Engine:
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.__session = session_make()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> None:
        if self.__session:
            if exc_type is not None:
                # An exception occurred, rollback the transaction
                try:
                    self.__session.rollback()
                except SQLAlchemyError:
                    pass
            try:
                self.__session.close()
            except SQLAlchemyError:
                pass
            finally:
                self.__session = None

    @contextmanager
    def transaction(self):
        """Context manager for transaction handling."""
        try:
            yield self
            if self.__session:
                self.__session.commit()
        except Exception as error:
            if self.__session:
                self.__session.rollback()
            raise error
