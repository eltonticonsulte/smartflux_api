# -*- coding: utf-8 -*-
from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from src.enums import DataFilterTimer


class CountGrupData(BaseModel):
    people_in: int
    people_out: int
    date: str


class CountGrupCode(BaseModel):
    people_in: int
    people_out: int
    code: str


class LineGraph(BaseModel):
    label: List[str]
    people_in: List[int]
    people_out: List[int]


class ResponseGrupDataCode(BaseModel):
    table: List[CountGrupCode]
    linegraph: LineGraph


class ResponseGrupData(BaseModel):
    table: List[CountGrupData]
    linegraph: LineGraph


class RequestVisitor(BaseModel):
    start_data: date
    end_data: Optional[date] = None
    grup: Optional[DataFilterTimer] = DataFilterTimer.AUTO_SELECT
    zone: Optional[str] = None
    device: Optional[str] = None


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
