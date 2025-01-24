# -*- coding: utf-8 -*-
from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from src.enums import CameraState


class RequestPing(BaseModel):
    channel_id: UUID
    status: CameraState
    worker_id: str


class RequestCreateCamera(BaseModel):
    name: str
    filal_id: int
    tag: Optional[str] = ""


class ResponseCamera(BaseModel):
    channel_id: UUID
    name: str
    filial_id: int
    status: CameraState
    tag: str


class RequestUpdateCamera(BaseModel):
    name: Optional[str] = None
    tag: Optional[str] = None
    filial_id: Optional[int] = None
    status: Optional[CameraState] = None
    metadate: Optional[dict] = None
