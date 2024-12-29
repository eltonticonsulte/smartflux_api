# -*- coding: utf-8 -*-
from ..database import Zone
from ..dto import CreateZoneRequest, CreateZoneResponse, GetZoneResponse


class ZoneMapper:
    @staticmethod
    def create_request_to_entity(request: CreateZoneRequest) -> Zone:
        return Zone(name=request.name, filial_id=request.filial_id)

    @staticmethod
    def create_entity_to_response(entity: Zone) -> GetZoneResponse:
        return GetZoneResponse(zone_id=entity.zone_id, name=entity.name)

    @staticmethod
    def get_entity_to_response(entity: Zone) -> GetZoneResponse:
        return GetZoneResponse(
            zone_id=entity.zone_id, name=entity.name, filial_id=entity.filial_id
        )
