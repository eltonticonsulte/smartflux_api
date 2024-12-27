# -*- coding: utf-8 -*-
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid
from ..common import UserRole


class CameraDTO:
    def __init__(
        self,
        channel_id: int,
        name: str,
        zona_id: int,
        metadate: dict,
    ):
        self.channel_id = channel_id
        self.name = name
        self.zona_id = zona_id
        self.metadate = metadate

    def __repr__(self):
        return f"ZoneDTO(channel_id={self.channel_id}, name={self.name}, zona_id={self.zona_id}, metadate={self.metadate})"


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
