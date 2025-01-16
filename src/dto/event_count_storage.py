# -*- coding: utf-8 -*-
from pydantic import BaseModel


class TotalCountGrupZone(BaseModel):
    zone_name: str
    total_count_in: int
    total_count_out: int


class TotalCountGrupHour(BaseModel):
    hour: str
    total_count_in: int
    total_count_out: int


class TotalCountGrupCamera(BaseModel):
    camera: str
    total_count_in: int
    total_count_out: int


class TotalCountGroupDay(BaseModel):
    day: str
    total_count_in: int
    total_count_out: int
