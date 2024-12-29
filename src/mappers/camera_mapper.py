# -*- coding: utf-8 -*-
from ..database import Camera
from ..dto import CameraDTO, CreateRequestCamera


class CameraMapper:
    @staticmethod
    def create_request_to_entity(new_camera: CreateRequestCamera) -> Camera:
        return Camera(name=new_camera.name, zona_id=new_camera.zona_id)

    @staticmethod
    def to_dto(camera: Camera) -> CameraDTO:
        return CameraDTO(
            channel_id=camera.channel_id,
            name=camera.name,
            zona_id=camera.zona_id,
            metadate=camera.metadate,
        )

    @staticmethod
    def to_entity(user: CameraDTO) -> Camera:
        return Camera(
            channel_id=user.channel_id,
            name=user.name,
            zona_id=user.zona_id,
            metadate=user.metadate,
        )
