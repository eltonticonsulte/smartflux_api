# -*- coding: utf-8 -*-
import logging
import uuid
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from ..database import Camera, DBConnectionHandler, IntegrityError, EventCountTemp
from .base_repository import BaseRepository
from ..dto import CameraDTO
from ..mappers import CameraMapper


class RepositoryCameraExeption(Exception):
    def __init__(self, message):
        super().__init__(message)


class CameraRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, camera: Camera) -> int:
        self.log.debug(f"create {camera}")
        with DBConnectionHandler() as session:
            try:
                session.add(camera)
                session.commit()
                return camera.camera_id
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

    def validade_token(self, token: uuid.UUID) -> bool:
        with DBConnectionHandler() as session:
            try:
                result = (
                    session.query(Camera).filter(Camera.channel_id == token).first()
                )
                if result is None:
                    raise RepositoryCameraExeption(f"Invalid token {token}")
            except Exception as error:
                self.log.error(error)
                raise RepositoryCameraExeption(f"Invalid token {token}")

    def add_all(self, events: List[EventCountTemp]):
        with DBConnectionHandler() as db:
            try:
                db.bulk_save_objects(events)
                db.commit()
            except Exception as error:
                db.rollback()
                raise error
