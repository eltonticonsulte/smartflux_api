# -*- coding: utf-8 -*-
import uuid
from src.database import Camera
from src.enums import CameraState
from src.dto import (
    RequestCreateCamera,
    ResponseCamera,
    RequestUpdateCamera,
    RequestStatus,
)


class CameraMapper:
    @staticmethod
    def create_request_to_entity(new_camera: RequestCreateCamera) -> Camera:
        if new_camera.tag is None or new_camera.tag == "":
            new_camera.tag = new_camera.name
        return Camera(
            name=new_camera.name, filial_id=new_camera.filal_id, tag=new_camera.tag
        )

    @staticmethod
    def update_status_to_entity(data: RequestStatus):
        camera = Camera(channel_id=data.channel_id, status=data.status)
        if data.worker_id:
            camera.worker_id = data.worker_id
        return camera

    @staticmethod
    def get_entity_to_response(entity: Camera) -> ResponseCamera:
        return ResponseCamera(
            channel_id=entity.channel_id,
            name=entity.name,
            worker_id="" if entity.worker_id is None else entity.worker_id,
            tag=entity.tag,
            filial_id=entity.filial_id,
            status=entity.status,
        )

    @staticmethod
    def update_request_to_entity(
        channel_id: uuid.UUID, request: RequestUpdateCamera
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
