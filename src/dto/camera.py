# -*- coding: utf-8 -*-
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class CreateCameraRequest(BaseModel):
    name: str
    zone_id: int


class CreateCameraResponse(BaseModel):
    channel_id: UUID
    name: str


class GetCameraResponse(BaseModel):
    channel_id: UUID
    name: str
    status: bool
    zone_id: int


class UpdateCameraRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None
    metadate: Optional[dict] = None
