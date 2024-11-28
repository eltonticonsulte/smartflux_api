# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import List


class EventReciver(BaseModel):
    event_id: int
    process_id: int
    token_api: str
    event_time: str
    count_in: int
    count_out: int


class PullEventReciver(BaseModel):
    data: List[EventReciver]
