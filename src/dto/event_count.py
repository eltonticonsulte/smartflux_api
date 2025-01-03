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


class TotalCount(BaseModel):
    total_count_in: int
    total_count_out: int
