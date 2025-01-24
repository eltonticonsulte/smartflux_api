# -*- coding: utf-8 -*-
from pydantic import BaseModel


class ResponseTotalCountGrupZone(BaseModel):
    zone_name: str
    total_count_in: int
    total_count_out: int


class ResponseTotalCountGrupHour(BaseModel):
    hour: str
    total_count_in: int
    total_count_out: int


class ResponseTotalCountGrupCamera(BaseModel):
    camera: str
    total_count_in: int
    total_count_out: int


class ResponseTotalCountGroupDay(BaseModel):
    day: str
    total_count_in: int
    total_count_out: int
