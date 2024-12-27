# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class InterfaceAuthController(ABC):
    @abstractmethod
    def login(self, name: str, password: str):
        pass

    @abstractmethod
    def current_user(self, token: str):
        pass


class InterfaceEmpresaController(ABC):
    @abstractmethod
    def create(self, name: str):
        pass


class InterfaceFilialController(ABC):
    @abstractmethod
    def create(self, name: str, cnpj: str, empresa_id: int):
        pass


class InterfaceZoneController(ABC):
    @abstractmethod
    def create(self, name: str):
        pass


class InterfaceCameraController(ABC):
    @abstractmethod
    def create(self, name: str):
        raise NotImplementedError("Method not implemented")

    def get_by_name(self, name: str):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def validate_token(self, token: str):
        raise NotImplementedError("Method not implemented")
