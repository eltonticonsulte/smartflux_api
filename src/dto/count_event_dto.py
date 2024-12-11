# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import List, Optional


class CountEventDTO(BaseModel):
    event_id: Optional[int]
    channel_id: str
    event_time: str
    count_in: int
    count_out: int
    camera_id: Optional[int]

    def to_dict(self):
        return self.model_dump()


class PullCountEventDTO(BaseModel):
    events: List[CountEventDTO]
