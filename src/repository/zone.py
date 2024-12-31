# -*- coding: utf-8 -*-
import logging
from typing import List
from ..database import Zone, DBConnectionHandler, IntegrityError


class RepositoryZoneExcption(Exception):
    def __init__(self, message):
        self.message = message


class ZoneRepository:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, zone: Zone) -> bool:
        self.log.debug(f"create zone {zone.name}")
        with DBConnectionHandler() as session:
            try:
                session.add(zone)
                session.commit()
                return zone.zone_id
            except IntegrityError as error:
                self.log.error(error, exc_info=error)
                raise RepositoryZoneExcption(
                    f"Zone {zone.name} already exists"
                ) from error
            except Exception as error:
                self.log.critical(error)
                raise error

    def get_by_name(self, name: str) -> Zone:
        with DBConnectionHandler() as session:
            zone = session.query(Zone).filter(Zone.name == name).one_or_none()
            if zone is None:
                raise RepositoryZoneExcption(f"Zone {name} not found")
            return zone

    def get_by_id(self, zone_id: int) -> Zone:
        with DBConnectionHandler() as session:
            zone = session.query(Zone).filter(Zone.zone_id == zone_id).one_or_none()
            if zone is None:
                raise RepositoryZoneExcption(f"Zone {zone_id} not found")
            return zone

    def get_all(self) -> List[Zone]:
        with DBConnectionHandler() as session:
            zonas = session.query(Zone).all()
            return zonas

    def update(self, zone: Zone) -> None:
        with DBConnectionHandler() as session:
            try:
                session.merge(zone)
                session.commit()
            except Exception as error:
                session.rollback()
                raise error

    def delete(self, zone_id: int) -> None:
        with DBConnectionHandler() as session:
            try:
                session.query(Zone).filter(Zone.zone_id == zone_id).delete()
                session.commit()
            except Exception as error:
                session.rollback()
                raise error
