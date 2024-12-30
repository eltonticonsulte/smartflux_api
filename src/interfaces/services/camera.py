# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import CreateCameraRequest, CreateCameraResponse, GetCameraResponse


class InterfaceCameraService(ABC):
    @abstractmethod
    def create(self, request: CreateCameraRequest) -> CreateCameraResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[GetCameraResponse]:
        raise NotImplementedError("Method not implemented")

    def get_by_name(self, name: str) -> GetCameraResponse:
        pass

    @abstractmethod
    def get_all_channels(self) -> List[str]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def validate_token(self, token: str):
        raise NotImplementedError("Method not implemented")
