# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import CreateZoneRequest, CreateZoneResponse, GetZoneResponse


class InterfaceZoneService(ABC):
    @abstractmethod
    def create(self, request: CreateZoneRequest) -> CreateZoneResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[GetZoneResponse]:
        raise NotImplementedError("Method not implemented")
