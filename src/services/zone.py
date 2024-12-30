# -*- coding: utf-8 -*-
import logging
from typing import List
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from core import get_settings
from ..repository import ZoneRepository
from ..dto import (
    CreateZoneRequest,
    GetZoneResponse,
    UpdateZoneRequest,
)
from ..interfaces import InterfaceZoneService
from ..mappers import ZoneMapper


class ZoneServices(InterfaceZoneService):
    def __init__(self, repository: ZoneRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, request: CreateZoneRequest) -> GetZoneResponse:
        self.log.debug(f"create_zone {request.name}")
        zone = ZoneMapper.create_request_to_entity(request)
        zone_id = self.repository.create(zone)
        entity = self.repository.get_by_id(zone_id)
        return ZoneMapper.get_entity_to_response(entity)

    def get_all(self) -> List[GetZoneResponse]:
        zonas = self.repository.get_all()
        result = [ZoneMapper.get_entity_to_response(zone) for zone in zonas]
        return result

    def update(self, id: int, request: UpdateZoneRequest) -> GetZoneResponse:
        zone = ZoneMapper.update_request_to_entity(id, request)
        self.repository.update(zone)
        result = self.repository.get_by_id(id)
        return ZoneMapper.get_entity_to_response(result)

    def delete(self, id: int) -> None:
        self.repository.delete(id)
