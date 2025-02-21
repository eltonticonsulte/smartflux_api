# -*- coding: utf-8 -*-
from typing import List
from pydantic import BaseModel


class CountGrup(BaseModel):
    people_in: int
    people_out: int
    hour: str


class LineGraph(BaseModel):
    label: List[str]
    people_int: List[int]
    people_out: List[int]


class ResponseGrupData(BaseModel):
    table: List[CountGrup]
    linegraph: LineGraph


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
