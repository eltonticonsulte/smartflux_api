# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import (
    CreateZoneRequest,
    CreateZoneResponse,
    GetZoneResponse,
    UpdateZoneRequest,
)


class InterfaceZoneService(ABC):
    @abstractmethod
    def create(self, request: CreateZoneRequest) -> CreateZoneResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[GetZoneResponse]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def update(self, id: int, request: UpdateZoneRequest) -> GetZoneResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError("Method not implemented")
