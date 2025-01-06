# -*- coding: utf-8 -*-
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from ..common import CameraState


class CreateCameraRequest(BaseModel):
    name: str
    zone_id: int


class GetCameraResponse(BaseModel):
    channel_id: UUID
    name: str
    status: CameraState
    zone_id: int


class UpdateCameraRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[CameraState] = None
    metadate: Optional[dict] = None
