# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from ..dto import (
    UserResponseAuth,
    CreateRequestCamera,
    CreateEmpresaRequest,
    CreateEmpresaResponse,
    GetEmpresaResponse,
    CreateFilialRequest,
    CreateFilialResponse,
    GetFilialResponse,
)


class InterfaceAuthService(ABC):
    @abstractmethod
    def auth_user(self, name: str, password: str) -> UserResponseAuth:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def current_user(self, token: str):
        raise NotImplementedError("Method not implemented")


class InterfaceEmpresaService(ABC):
    @abstractmethod
    def create(self, empresa: CreateEmpresaRequest) -> CreateEmpresaResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[GetEmpresaResponse]:
        raise NotImplementedError("Method not implemented")


class InterfaceFilialService(ABC):
    @abstractmethod
    def create(self, resquest: CreateFilialRequest) -> CreateFilialResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[GetFilialResponse]:
        raise NotImplementedError("Method not implemented")


class InterfaceZoneService(ABC):
    @abstractmethod
    def create(self, name: str, filial_id: int):
        raise NotImplementedError("Method not implemented")


class InterfaceCameraService(ABC):
    @abstractmethod
    def create(self, request: CreateRequestCamera):
        raise NotImplementedError("Method not implemented")

    def get_by_name(self, name: str):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def validate_token(self, token: str):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def register_event(self, data):
        raise NotImplementedError("Method not implemented")