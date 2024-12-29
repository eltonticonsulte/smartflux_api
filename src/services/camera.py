# -*- coding: utf-8 -*-
import logging
import uuid
from typing import List
from ..repository import CameraRepository
from ..dto import (
    CreateCameraRequest,
    CreateCameraResponse,
    GetCameraResponse,
)
from ..mappers import CameraMapper


class CameraServices:
    def __init__(self, repository: CameraRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, request: CreateCameraRequest) -> CreateCameraResponse:
        new_camera = CameraMapper.create_request_to_entity(request)
        camera_id = self.repository.create(new_camera)
        return CreateCameraResponse(camera_id=camera_id, name=new_camera.name)

    def get_all(self) -> List[GetCameraResponse]:
        datas = self.repository.get_all()
        result = [CameraMapper.get_entity_to_response(camera) for camera in datas]
        return result

    def get_all_channels(self) -> List[uuid.UUID]:
        datas = self.repository.get_all()
        result = [camera.channel_id for camera in datas]
        return result

    def validate_channel_id(self, channel_id: uuid.UUID):
        self.log.debug(f"validate_channel_id {channel_id}")
        self.repository.get_by_channel_id(channel_id)
