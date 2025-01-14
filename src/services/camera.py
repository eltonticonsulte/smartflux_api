# -*- coding: utf-8 -*-
import logging
import uuid
from typing import List
from src.repository import CameraRepository
from src.dto import (
    CreateCameraRequest,
    GetCameraResponse,
    UpdateCameraRequest,
)
from src.mappers import CameraMapper
from src.interfaces import InterfaceCameraService


class CameraServices(InterfaceCameraService):
    def __init__(self, repository: CameraRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, request: CreateCameraRequest) -> GetCameraResponse:
        new_camera = CameraMapper.create_request_to_entity(request)
        channel_id = self.repository.create(new_camera)
        entity = self.repository.get_by_channel_id(channel_id)
        return CameraMapper.get_entity_to_response(entity)

    def get_all(self) -> List[GetCameraResponse]:
        datas = self.repository.get_all()
        result = [CameraMapper.get_entity_to_response(camera) for camera in datas]
        return result

    def get_all_channels(self) -> List[uuid.UUID]:
        datas = self.repository.get_all()
        result = [camera.channel_id for camera in datas]
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
        self, channel_id: uuid.UUID, request: UpdateCameraRequest
    ) -> GetCameraResponse:

        camera = CameraMapper.update_request_to_entity(channel_id, request)
        self.repository.update(camera)
        camera_updated = self.repository.get_by_channel_id(channel_id)
        self.log.debug(f"updated {camera_updated}")
        return CameraMapper.get_entity_to_response(camera_updated)
