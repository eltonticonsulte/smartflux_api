# -*- coding: utf-8 -*-

from logging import getLogger
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy import func, case
from .connect import DBConnectionHandler
from .schema import Filial, Camera, Zone, EventCountTemp, Empresa, EventCountHourly


class DataBase:
    def __init__(self) -> None:
        self.log = getLogger(__name__)

    def insert_empresa(self, empresa: Empresa) -> int:
        with DBConnectionHandler() as session:
            try:
                session.add(empresa)
                session.commit()
                return empresa.id
            except Exception as error:
                session.rollback()
                raise error

    def update_empresa(self, empresa: Empresa) -> int:
        with DBConnectionHandler() as db:
            try:
                db.merge(empresa)
                db.commit()
                return empresa.id
            except Exception as error:
                db.rollback()
                raise error

    def select_empresa_all(self) -> List[Empresa]:
        with DBConnectionHandler() as db:
            try:
                return db.query(Empresa).all()
            except Exception as error:
                db.rollback()
                raise error

    def delete_empresa(self, empresa_id: int) -> None:
        with DBConnectionHandler() as db:
            try:
                db.query(Empresa).filter(Empresa.id == empresa_id).delete()
                db.commit()
            except Exception as error:
                db.rollback()
                raise error

    def insert_filial(self, filial: Filial) -> int:
        with DBConnectionHandler() as db:
            try:
                db.add(filial)
                db.commit()
                return filial.id
            except Exception as error:
                db.rollback()
                raise error

    def select_filial_all(self) -> List[Filial]:
        with DBConnectionHandler() as db:
            try:
                return db.query(Filial).all()
            except Exception as error:
                db.rollback()
                raise error

    def delete_filial(self, filial_id: int) -> None:
        with DBConnectionHandler() as db:
            try:
                db.query(Filial).filter(Filial.id == filial_id).delete()
                db.commit()
            except Exception as error:
                db.rollback()
                raise error

    def insert_zone(self, zone: Zone) -> int:
        with DBConnectionHandler() as db:
            try:
                db.add(zone)
                db.commit()
                return zone.id
            except Exception as error:
                db.rollback()
                raise error

    def select_zona_all(self) -> List[Zone]:
        with DBConnectionHandler() as db:
            try:
                return db.query(Zone).all()
            except Exception as error:
                db.rollback()
                raise error

    def delete_zone(self, zone_id: int) -> None:
        with DBConnectionHandler() as db:
            try:
                db.query(Zone).filter(Zone.id == zone_id).delete()
                db.commit()
            except Exception as error:
                db.rollback()
                raise error

    def insert_camera(self, camera: Camera) -> int:
        with DBConnectionHandler() as db:
            try:
                db.add(camera)
                db.commit()
                return camera.id
            except Exception as error:
                db.rollback()
                raise error

    def select_camera_all(self) -> List[Camera]:
        with DBConnectionHandler() as db:
            try:
                return db.query(Camera).all()
            except Exception as error:
                db.rollback()
                raise error

    def delete_camera(self, camera_id: int) -> None:
        with DBConnectionHandler() as db:
            try:
                db.query(Camera).filter(Camera.id == camera_id).delete()
                db.commit()
            except Exception as error:
                db.rollback()
                raise error

    def insert_event_count_temp(self, event_count_temp: EventCountTemp) -> int:
        with DBConnectionHandler() as db:
            try:
                db.add(event_count_temp)
                db.commit()
                return event_count_temp.id
            except Exception as error:
                db.rollback()
                raise error

    def select_event_count_temp_all(self) -> List[EventCountTemp]:
        with DBConnectionHandler() as db:
            try:
                return db.query(EventCountTemp).all()
            except Exception as error:
                db.rollback()
                raise error

    def delete_event_count_temp(self, event_count_temp_id: int) -> None:
        with DBConnectionHandler() as db:
            try:
                db.query(EventCountTemp).filter(
                    EventCountTemp.id == event_count_temp_id
                ).delete()
                db.commit()
            except Exception as error:
                db.rollback()
                raise error
