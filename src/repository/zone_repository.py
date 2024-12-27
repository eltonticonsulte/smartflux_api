# -*- coding: utf-8 -*-
import logging
from typing import List
from ..database import Zone, DBConnectionHandler, IntegrityError
from .base_repository import BaseRepository
from ..dto import ZoneDTO
from ..mappers import ZoneMapper


class RepositoryZoneExcption(Exception):
    def __init__(self, message):
        self.message = message


class ZoneRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, user: ZoneDTO) -> bool:
        self.log.debug(f"create_user {user}")
        try:
            db_zone = ZoneMapper.to_entity(user)
            result: Zone = self.add(db_zone)
            return result.zone_id
        except IntegrityError:
            raise RepositoryZoneExcption(f"Zone {user.name} already exists")
        except Exception as error:
            self.log.critical(error)
            raise error

    def get_by_name(self, name: str) -> ZoneDTO:
        with DBConnectionHandler() as session:
            zone = session.query(Zone).filter(Zone.name == name).one_or_none()
            if zone is None:
                raise RepositoryZoneExcption(f"Zone {name} not found")
            return ZoneMapper.to_dto(zone)

    def get_all(self) -> List[ZoneDTO]:
        with DBConnectionHandler() as session:
            zonas = session.query(Zone).all()
            return [ZoneMapper.to_dto(zone) for zone in zonas]
