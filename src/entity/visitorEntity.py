# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional
from typing import List


class EventReciver(BaseModel):
    event_id: int
    channel_id: int
    token_api: str
    event_time: str
    count_in: int
    count_out: int


class PullEventReciver(BaseModel):
    data: List[EventReciver]


class UserReciver(BaseModel):
    username: str
    description: Optional[str]
    password: str
