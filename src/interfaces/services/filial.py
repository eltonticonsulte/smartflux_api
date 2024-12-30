# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import (
    CreateFilialRequest,
    CreateFilialResponse,
    GetFilialResponse,
    UpdateFilialRequest,
)


class InterfaceFilialService(ABC):
    @abstractmethod
    def create(self, resquest: CreateFilialRequest) -> CreateFilialResponse:
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
