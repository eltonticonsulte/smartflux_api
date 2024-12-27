# -*- coding: utf-8 -*-
from uuid import UUID
from datetime import datetime


class CountEventDTO:
    def __init__(
        self,
        channel_id: UUID,
        event_id: int,
        event_time: datetime,
        count_in: int,
        count_out: int,
    ):
        self.channel_id = channel_id
        self.event_time = event_time
        self.count_in = count_in
        self.event_id = event_id
        self.count_out = count_out

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "event_time": self.event_time,
            "count_in": self.count_in,
            "event_id": self.event_id,
            "count_out": self.count_out,
        }

    def __repr__(self):
        return f"CountEventDTO(channel_id={self.channel_id}, event_time={self.event_time}, count_in={self.count_in}, event_id={self.event_id}, count_out={self.count_out})"
