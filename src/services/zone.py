# -*- coding: utf-8 -*-
import logging
from typing import List
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from core import get_settings
from ..repository import ZoneRepository
from ..dto import CreateZoneRequest, CreateZoneResponse, GetZoneResponse
from ..mappers import ZoneMapper


class ZoneServices:
    def __init__(self, repository: ZoneRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, request: CreateZoneRequest) -> bool:
        self.log.debug(f"create_zone {request.name}")
        zone = ZoneMapper.create_request_to_entity(request)
        zone_id = self.repository.create(zone)
        return CreateZoneResponse(zone_id=zone_id, name=zone.name)

    # def get_by_name(self, name: str) -> Zone:
    #    return self.repository.get_by_name(name)

    def get_all(self) -> List[GetZoneResponse]:
        zonas = self.repository.get_all()
        result = [ZoneMapper.get_entity_to_response(zone) for zone in zonas]
        return result
