# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import CreateEmpresaRequest, GetEmpresaResponse


class InterfaceEmpresaService(ABC):
    @abstractmethod
    def create(self, empresa: CreateEmpresaRequest) -> GetEmpresaResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[GetEmpresaResponse]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_by_id(self, id: int) -> GetEmpresaResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def update(self, id: int, empresa: CreateEmpresaRequest) -> GetEmpresaResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError("Method not implemented")