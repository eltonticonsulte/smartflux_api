# -*- coding: utf-8 -*-
from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel


class EventCountResponse(BaseModel):
    event_id: int
    status: bool
    description: Optional[str]


class EventCountRequest(BaseModel):
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


class TotalCount(BaseModel):
    total_count_in: int
    total_count_out: int
