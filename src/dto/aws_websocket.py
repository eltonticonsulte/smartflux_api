# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EventCountSendWebsocket(BaseModel):
    camera_name: str
    zone_name: str
    count_in: int
    count_out: int
    event_time: datetime
    description: Optional[str]

    def to_dict(self):
        return {
            "camera_name": self.camera_name,
            "zone_name": self.zone_name,
            "count_in": self.count_in,
            "count_out": self.count_out,
            "event_time": self.event_time.isoformat(),
            "description": self.description,
        }
