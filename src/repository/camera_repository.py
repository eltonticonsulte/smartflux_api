# -*- coding: utf-8 -*-
import logging
from typing import List
from ..database import Camera, DBConnectionHandler, IntegrityError
from .base_repository import BaseRepository
from ..dto import CameraDTO
from ..mappers import CameraMapper


class RepositoryCameraExeption(Exception):
    def __init__(self, message):
        super().__init__(message)


class CameraRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, camera: CameraDTO) -> bool:
        self.log.debug(f"create {camera}")
        db_camera = CameraMapper.to_entity(camera)
        try:
            return self.add(db_camera)
        except IntegrityError:
            raise RepositoryCameraExeption(f"Camera {camera.name} already exists")
        except Exception as error:
            self.log.error(error)
            raise error

    def get_by_name(self, name: str) -> CameraDTO:
        with DBConnectionHandler() as session:
            camera = session.query(Camera).filter(Camera.name == name).one_or_none()
            if camera is None:
                raise RepositoryCameraExeption(f"Camera {name} not found")
            return CameraMapper.to_dto(camera)

    def get_all(self) -> List[CameraDTO]:
        with DBConnectionHandler() as session:
            cameras = session.query(Camera).all()
            return [CameraMapper.to_dto(camera) for camera in cameras]
