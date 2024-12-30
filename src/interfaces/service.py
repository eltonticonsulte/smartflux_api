# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from ..dto import (
    AuthUserResponse,
    AuthUserRequest,
    CreateCameraRequest,
    CreateCameraResponse,
    GetCameraResponse,
    EventCountRequest,
    EventCountResponse,
    CreateEmpresaRequest,
    CreateEmpresaResponse,
    GetEmpresaResponse,
    CreateFilialRequest,
    CreateFilialResponse,
    GetFilialResponse,
    CreateZoneRequest,
    CreateZoneResponse,
    GetZoneResponse,
)


class InterfaceUserService(ABC):
    @abstractmethod
    def auth_user(self, request: AuthUserRequest) -> AuthUserResponse:
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

    @abstractmethod
    def get_by_id(self, id: int) -> GetEmpresaResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def update(self, id: int, empresa: CreateEmpresaRequest) -> GetEmpresaResponse:
        raise NotImplementedError("Method not implemented")


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


class InterfaceZoneService(ABC):
    @abstractmethod
    def create(self, request: CreateZoneRequest) -> CreateZoneResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[GetZoneResponse]:
        raise NotImplementedError("Method not implemented")


class InterfaceCameraService(ABC):
    @abstractmethod
    def create(self, request: CreateCameraRequest) -> CreateCameraResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[GetCameraResponse]:
        raise NotImplementedError("Method not implemented")

    def get_by_name(self, name: str):
        pass

    @abstractmethod
    def get_all_channels(self):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def validate_token(self, token: str):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create(self, data):
        raise NotImplementedError("Method not implemented")


class InterfaceEventCountService(ABC):
    @abstractmethod
    def insert_pull(
        self, request: List[EventCountRequest], channels: List[UUID]
    ) -> List[EventCountResponse]:
        raise NotImplementedError("Method not implemented")
