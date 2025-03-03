# -*- coding: utf-8 -*-
from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel


class EventCountDataValidate(BaseModel):
    event_id: int
    camera_name: str
    channel_id: uuid.UUID
    zone_name: str
    count_in: int
    count_out: int
    event_time: datetime
    status: bool
    description: Optional[str]

    def to_websocket(self):
        return {
            "event_id": self.event_id,
            "camera_name": self.camera_name,
            "zone_name": self.zone_name,
            "count_in": self.count_in,
            "count_out": self.count_out,
            "event_time": self.event_time.isoformat(),
            "description": self.description,
        }


class ResponseEventCount(BaseModel):
    event_id: int
    status: bool
    description: Optional[str]


class RequestEventCount(BaseModel):
    event_id: int
    channel_id: uuid.UUID
    event_time: datetime
    count_in: int
    count_out: int

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "channel_id": str(self.channel_id),
            "event_time": self.event_time.isoformat(),
            "count_in": self.count_in,
            "count_out": self.count_out,
        }


class ResponseTotalCount(BaseModel):
    total_count_in: int
    total_count_out: int
    max_count_day: int
