# -*- coding: utf-8 -*-
import logging
from typing import List
from ..database import (
    Zone,
    DBConnectionHandler,
)
from .base_repository import BaseRepository
from ..dto import ZoneDTO
from ..mappers import ZoneMapper


class ZoneRepository(BaseRepository):
    def __init__(self):

        self.log = logging.getLogger(__name__)

    def create(self, user: ZoneDTO) -> bool:
        self.log.debug(f"create_user {user}")
        db_zone = ZoneMapper.to_entity(user)
        return self.add(db_zone)

    def get_by_name(self, name: str) -> ZoneDTO:
        try:
            with DBConnectionHandler() as session:
                zone = session.query(Zone).filter(Zone.name == name).one_or_none()
                if zone is None:
                    raise ValueError("Zone not found")
                return ZoneMapper.to_dto(zone)
        except Exception as error:
            self.log.critical(error)
            raise error

    def get_all(self) -> List[ZoneDTO]:
        try:
            with DBConnectionHandler() as session:
                zonas = session.query(Zone).all()
                return [ZoneMapper.to_dto(zone) for zone in zonas]
        except Exception as error:
            self.log.critical(error)
            raise error
