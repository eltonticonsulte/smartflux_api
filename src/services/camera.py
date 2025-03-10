# -*- coding: utf-8 -*-
import logging
import uuid
from typing import List
from src.repository import CameraRepository
from src.dto import (
    RequestCreateCamera,
    ResponseCamera,
    RequestUpdateCamera,
    RequestStatus,
    ResponseCameraList,
)
from src.mappers import CameraMapper
from src.interfaces import InterfaceCameraService


class CameraServices(InterfaceCameraService):
    def __init__(self, repository: CameraRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, request: RequestCreateCamera) -> ResponseCamera:
        self.log.debug(f"create_camera {request}")
        new_camera = CameraMapper.create_request_to_entity(request)
        channel_id = self.repository.create(new_camera)
        entity = self.repository.get_by_channel_id(channel_id)
        return CameraMapper.get_entity_to_response(entity)

    def update_status(self, data: RequestStatus) -> None:
        entity = CameraMapper.update_status_to_entity(data)
        self.repository.update_status(entity)

    def get_all(self) -> List[ResponseCamera]:
        datas = self.repository.get_all()
        result = [CameraMapper.get_entity_to_response(camera) for camera in datas]
        return result

    def get_all_channels(self) -> List[uuid.UUID]:
        datas = self.repository.get_all()
        result = [camera.channel_id for camera in datas]
        return result

    def get_list_by_filial(self, filial_id: int) -> List[ResponseCameraList]:
        datas = self.repository.get_by_filial(filial_id)
        result = [CameraMapper.get_entity_to_response_list(camera) for camera in datas]
        return result

    def get_list_name_camera_by_filial(self, filial_id: int) -> List[str]:
        datas = self.repository.get_by_filial(filial_id)
        result = [camera.name for camera in datas]
        result.sort(key=str.lower)
        return result

    def get_list_tag_by_filial(self, filial_id: int) -> List[str]:
        datas = self.repository.get_by_filial(filial_id)
        result = list(set(camera.tag for camera in datas))
        result.sort(key=str.lower)
        return result

    def get_channel_by_filial(self, filial_id: int) -> List[uuid.UUID]:
        datas = self.repository.get_by_filial(filial_id)
        result = [camera.channel_id for camera in datas]
        return result

    def delete(self, channel_id: uuid.UUID):
        self.log.debug(f"delete {channel_id}")
        self.repository.delete(channel_id)

    def validate_channel_id(self, channel_id: uuid.UUID):
        self.log.debug(f"validate_channel_id {channel_id}")
        self.repository.get_by_channel_id(channel_id)

    def update(
        self, channel_id: uuid.UUID, request: RequestUpdateCamera
    ) -> ResponseCamera:

        camera = CameraMapper.update_request_to_entity(channel_id, request)
        self.repository.update(camera)
        camera_updated = self.repository.get_by_channel_id(channel_id)
        self.log.debug(f"updated {camera_updated}")
        return CameraMapper.get_entity_to_response(camera_updated)
