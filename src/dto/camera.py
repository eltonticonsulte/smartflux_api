# -*- coding: utf-8 -*-
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from ..enums import CameraState


class CreateCameraRequest(BaseModel):
    name: str
    tag: Optional[str] = ""


class GetCameraResponse(BaseModel):
    channel_id: UUID
    name: str
    status: CameraState
    tag: str


class UpdateCameraRequest(BaseModel):
    name: Optional[str] = None
    tag: Optional[str] = None
    status: Optional[CameraState] = None
    metadate: Optional[dict] = None
