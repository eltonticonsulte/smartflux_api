# -*- coding: utf-8 -*-
from pydantic import BaseModel
from enum import Enum


class RuleName(Enum):
    ENTER = "Enter"
    EXIT = "Exit"


class EventReciver(BaseModel):
    channel_id: int
    channel_name: str
    event_name: str
    event_origin: str
    event_type: str
    event_time: str
    object_id: str
    rule_id: int
    rule_name: RuleName
