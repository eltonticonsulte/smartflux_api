# -*- coding: utf-8 -*-
from ..database import Zone
from ..dto import ZoneDTO


class ZoneMapper:
    @staticmethod
    def to_dto(user: Zone) -> ZoneDTO:
        return ZoneDTO(name=user.name, filial_id=user.filial_id)

    @staticmethod
    def to_entity(user: ZoneDTO) -> Zone:
        return Zone(name=user.name, filial_id=user.filial_id)
