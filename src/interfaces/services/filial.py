# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import (
    CreateFilialRequest,
    GetFilialResponse,
    UpdateFilialRequest,
)


class InterfaceFilialService(ABC):
    @abstractmethod
    def create(self, resquest: CreateFilialRequest) -> GetFilialResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def validate_token(self, token: str):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[GetFilialResponse]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_by_id(self, id: int) -> GetFilialResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def update(self, filial_id: int, request: UpdateFilialRequest) -> GetFilialResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError("Method not implemented")
