# -*- coding: utf-8 -*-
from typing import Optional, Type, Any
from contextlib import contextmanager
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from core import get_settings


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__engine = create_engine(
            get_settings().DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=3600,
        )
        self.session: Optional[Session] = None

    @staticmethod
    def get_engine(url: str) -> Engine:
        return create_engine(url)

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self.session

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> None:
        if self.session:
            if exc_type is not None:
                # An exception occurred, rollback the transaction
                try:
                    self.session.rollback()
                except SQLAlchemyError:
                    pass
            try:
                self.session.close()
            except SQLAlchemyError:
                pass
            finally:
                self.session = None

    @contextmanager
    def transaction(self):
        """Context manager for transaction handling."""
        try:
            yield self
            if self.session:
                self.session.commit()
        except Exception as error:
            if self.session:
                self.session.rollback()
            raise error
