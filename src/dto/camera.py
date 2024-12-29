# -*- coding: utf-8 -*-
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid


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


class CountEventDTO(BaseModel):
    event_id: Optional[int]
    channel_id: uuid.UUID
    event_time: datetime
    count_in: int
    count_out: int

    def to_dict(self):
        return self.model_dump()

    def __repr__(self):
        return f"CountEventData(event_id={self.event_id}, channel_id={self.channel_id}, event_time={self.event_time}, count_in={self.count_in}, count_out={self.count_out})"
