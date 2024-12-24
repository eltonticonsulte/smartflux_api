# -*- coding: utf-8 -*-
import logging
from typing import List
from ..database import (
    Camera,
    DBConnectionHandler,
)
from .base_repository import BaseRepository
from ..dto import CameraDTO
from ..mappers import CameraMapper


class CameraRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, camera: CameraDTO) -> bool:
        self.log.debug(f"create {camera}")
        db_camera = CameraMapper.to_entity(camera)
        return self.add(db_camera)

    def get_by_name(self, name: str) -> CameraDTO:
        try:
            with DBConnectionHandler() as session:
                camera = session.query(Camera).filter(Camera.name == name).one_or_none()
                if camera is None:
                    raise ValueError("Camera not found")
                return CameraMapper.to_dto(camera)
        except Exception as error:
            self.log.critical(error)
            raise error

    def get_all(self) -> List[CameraDTO]:
        try:
            with DBConnectionHandler() as session:
                cameras = session.query(Camera).all()
                return [CameraMapper.to_dto(camera) for camera in cameras]
        except Exception as error:
            self.log.critical(error)
            raise error
