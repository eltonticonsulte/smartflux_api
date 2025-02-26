# -*- coding: utf-8 -*-
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel
from src.enums import CameraState


class RequestStatus(BaseModel):
    channel_id: UUID
    status: CameraState
    worker_id: Optional[str] = None


class RequestCreateCamera(BaseModel):
    name: str
    filal_id: int
    tag: Optional[str] = ""


class ResponseCamera(BaseModel):
    channel_id: UUID
    name: str
    worker_id: str
    filial_id: int
    status: CameraState
    tag: str


class ResponseCameraList(BaseModel):
    name: str
    zone: str


class ResponseCamerasName(BaseModel):
    label: str
    value: str


class DataComboZone(BaseModel):
    id: str
    name: str


class ResponseCamerasZone(BaseModel):
    page: Optional[int] = 1
    total: int
    items: List[DataComboZone]


class RequestUpdateCamera(BaseModel):
    name: Optional[str] = None
    tag: Optional[str] = None
    filial_id: Optional[int] = None
    status: Optional[CameraState] = None
    metadate: Optional[dict] = None
