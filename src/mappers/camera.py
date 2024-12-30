# -*- coding: utf-8 -*-
import uuid
from ..database import Camera
from ..dto import (
    CreateCameraRequest,
    GetCameraResponse,
    UpdateCameraRequest,
)


class CameraMapper:
    @staticmethod
    def create_request_to_entity(new_camera: CreateCameraRequest) -> Camera:
        return Camera(name=new_camera.name, zona_id=new_camera.zone_id)

    @staticmethod
    def get_entity_to_response(entity: Camera) -> GetCameraResponse:
        return GetCameraResponse(
            channel_id=entity.channel_id,
            name=entity.name,
            zone_id=entity.zona_id,
            status=entity.status,
        )

    @staticmethod
    def update_request_to_entity(
        channel_id: uuid.UUID, request: UpdateCameraRequest
    ) -> Camera:
        camera = Camera(channel_id=channel_id)
        if request.name:
            camera.name = request.name
        if request.status:
            camera.status = request.status
        if request.metadate:
            camera.metadate = request.metadate
        return camera
