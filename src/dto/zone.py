# -*- coding: utf-8 -*-
from pydantic import BaseModel


class CreateZoneRequest(BaseModel):
    name: str
    filial_id: int


class CreateZoneResponse(BaseModel):
    name: str
    zone_id: int


class GetZoneResponse(BaseModel):
    zone_id: int
    name: str
    filial_id: int
