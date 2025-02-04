# -*- coding: utf-8 -*-
import logging
import uuid
from typing import List
from src.database import Camera, DBConnectionHandler, IntegrityError, Filial
from src.mappers import CameraMapper


class RepositoryCameraExeption(Exception):
    def __init__(self, message):
        super().__init__(message)


class CameraRepository:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, camera: Camera) -> uuid.UUID:
        with DBConnectionHandler() as session:
            try:
                session.add(camera)
                session.commit()
                return camera.channel_id
            except IntegrityError as error:
                raise RepositoryCameraExeption(
                    f"Camera {camera.name} already exists {error}"
                ) from error
            except Exception as error:
                self.log.error(error)
                raise error

    def update_status(self, entity: Camera):
        with DBConnectionHandler() as session:
            session.merge(entity)
            session.commit()

    def get_by_name(self, name: str) -> Camera:
        with DBConnectionHandler() as session:
            camera = session.query(Camera).filter(Camera.name == name).one_or_none()
            if camera is None:
                raise RepositoryCameraExeption(f"Camera {name} not found")
            return CameraMapper.to_dto(camera)

    def get_all(self) -> List[Camera]:
        with DBConnectionHandler() as session:
            cameras = session.query(Camera).all()
            return cameras

    def get_by_filial(self, filial_id: int) -> List[Camera]:
        with DBConnectionHandler() as session:
            cameras = (
                session.query(Camera)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .filter(Filial.filial_id == filial_id)
                .all()
            )
            return cameras

    def get_by_channel_id(self, channel_id: uuid.UUID) -> Camera:
        with DBConnectionHandler() as session:
            return session.query(Camera).filter(Camera.channel_id == channel_id).first()

    def delete(self, channel_id: uuid.UUID):
        self.log.debug(f"delete {channel_id}")
        with DBConnectionHandler() as session:
            session.query(Camera).filter(Camera.channel_id == channel_id).delete()
            session.commit()

    def update(self, camera: Camera):
        with DBConnectionHandler() as session:
            try:
                session.merge(camera)
                session.commit()
            except Exception as error:
                session.rollback()
                self.log.error(error)
                raise error
