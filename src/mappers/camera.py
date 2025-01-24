# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from src.database import Camera
from src.enums import CameraState
from src.dto import (
    CreateCameraRequest,
    GetCameraResponse,
    UpdateCameraRequest,
    RequestPing
)


class CameraMapper:
    @staticmethod
    def create_request_to_entity(new_camera: CreateCameraRequest) -> Camera:
        if new_camera.tag is None or new_camera.tag == "":
            new_camera.tag = new_camera.name
        return Camera(
            name=new_camera.name, filial_id=new_camera.filal_id, tag=new_camera.tag
        )

    @staticmethod
    def update_ping_to_entity(data: RequestPing):
        return Camera(
            worker_id=data.worker_id, status=data.status, channel_id=data.channel_id
        )

    @staticmethod
    def get_entity_to_response(entity: Camera) -> GetCameraResponse:
        return GetCameraResponse(
            channel_id=entity.channel_id,
            name=entity.name,
            tag=entity.tag,
            filial_id=entity.filial_id,
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
        if request.filial_id:
            camera.filial_id = request.filial_id
        return camera
