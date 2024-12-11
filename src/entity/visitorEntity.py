# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import List


class EventReciver(BaseModel):
    event_id: int
    channel_id: int
    token_api: str
    event_time: str
    count_in: int
    count_out: int

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "channel_id": self.channel_id,
            "token_api": self.token_api,
            "event_time": self.event_time,
            "count_in": self.count_in,
            "count_out": self.count_out,
        }


class PullEventReciver(BaseModel):
    data: List[EventReciver]
