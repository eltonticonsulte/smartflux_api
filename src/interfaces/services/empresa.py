# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import RequestCreateEmpresa, ResponseEmpresa


class InterfaceEmpresaService(ABC):
    @abstractmethod
    def create(self, empresa: RequestCreateEmpresa) -> ResponseEmpresa:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[ResponseEmpresa]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_by_id(self, empresa_id: int) -> ResponseEmpresa:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def update(self, empresa_id: int, empresa: RequestCreateEmpresa) -> ResponseEmpresa:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def delete(self, empresa_id: int) -> None:
        raise NotImplementedError("Method not implemented")
