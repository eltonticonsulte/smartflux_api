# -*- coding: utf-8 -*-
from ..database import Camera
from ..dto import CameraDTO


class CameraMapper:
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
