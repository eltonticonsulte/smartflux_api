# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from src.dto import (
    RequestCreateCamera,
    ResponseCamera,
    RequestUpdateCamera,
    RequestStatus,
)


class InterfaceCameraService(ABC):
    @abstractmethod
    def create(self, request: RequestCreateCamera) -> ResponseCamera:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def update_status(self, data: RequestStatus) -> None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[ResponseCamera]:
        raise NotImplementedError("Method not implemented")

    def get_by_name(self, name: str) -> ResponseCamera:
        pass

    @abstractmethod
    def get_all_channels(self) -> List[str]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_channel_by_filial(self, filial_id: int) -> List[UUID]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_list_name_camera_by_filial(self, filial_id: int) -> List[str]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_list_tag_by_filial(self, filial_id: int) -> List[str]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def update(self, channel_id: UUID, request: RequestUpdateCamera) -> ResponseCamera:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def delete(self, channel_id: UUID) -> None:
        raise NotImplementedError("Method not implemented")
