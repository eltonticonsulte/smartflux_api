# -*- coding: utf-8 -*-
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid


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
