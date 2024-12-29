# -*- coding: utf-8 -*-
from pydantic import BaseModel


class CreateCameraRequest(BaseModel):
    name: str
    zone_id: int


class CreateCameraResponse(BaseModel):
    camera_id: int
    name: str


class GetCameraResponse(BaseModel):
    camera_id: int
    name: str
    zone_id: int
