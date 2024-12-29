# -*- coding: utf-8 -*-
from ..database import Camera
from ..dto import CreateCameraRequest, CreateCameraResponse, GetCameraResponse


class CameraMapper:
    @staticmethod
    def create_request_to_entity(new_camera: CreateCameraRequest) -> Camera:
        return Camera(name=new_camera.name, zona_id=new_camera.zone_id)

    @staticmethod
    def create_entity_to_response(entity: Camera) -> CreateCameraResponse:
        return CreateCameraResponse(camera_id=entity.camera_id, name=entity.name)

    @staticmethod
    def get_entity_to_response(entity: Camera) -> GetCameraResponse:
        return GetCameraResponse(
            camera_id=entity.camera_id, name=entity.name, zone_id=entity.zona_id
        )
