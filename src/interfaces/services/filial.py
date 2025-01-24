# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from src.dto import (
    RequestCreateFilial,
    ResponseFilial,
    RequestUpdateFilial,
)


class InterfaceFilialService(ABC):
    @abstractmethod
    def create(self, resquest: RequestCreateFilial) -> ResponseFilial:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def check_token(self, token: UUID) -> bool:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_by_token(self, token: UUID) -> ResponseFilial:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[ResponseFilial]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_by_id(self, filial_id: int) -> ResponseFilial:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def update(self, filial_id: int, request: RequestUpdateFilial) -> ResponseFilial:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def delete(self, filial_id: int) -> None:
        raise NotImplementedError("Method not implemented")
