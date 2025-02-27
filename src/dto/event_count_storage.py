# -*- coding: utf-8 -*-
from typing import List, Optional
from datetime import date
from pydantic import BaseModel, field_validator
from src.enums import FlagGrupDate, FlagGrupLabel


class CountGrupDate(BaseModel):
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


class ResponseGrupDataLabel(BaseModel):
    table: List[CountGrupCode]
    linegraph: LineGraph


class ResponseGrupData(BaseModel):
    table: List[CountGrupDate]
    linegraph: LineGraph


class ResponseGrupReport(BaseModel):
    data: str


class RequestVisitorGrupZone(BaseModel):
    start_data: date
    end_data: Optional[date] = None
    grup: Optional[FlagGrupDate] = FlagGrupDate.AUTO_SELECT

    @field_validator("end_data")
    def check_dates(cls, end_data, info):
        start_data = info.data.get("start_data")
        if end_data is None:
            end_data = start_data
        if end_data < start_data:
            raise ValueError("data final menor que data inicial")
        return end_data


class RequestVisitorDate(BaseModel):
    start_data: date
    end_data: Optional[date] = None
    grup: Optional[FlagGrupDate] = FlagGrupDate.AUTO_SELECT
    zone: Optional[str] = None
    device: Optional[str] = None

    @field_validator("end_data")
    def check_dates(cls, end_data, info):
        start_data = info.data.get("start_data")
        if end_data is None:
            end_data = start_data
        if end_data < start_data:
            raise ValueError("data final menor que data inicial")
        return end_data


class RequestVisitorLabel(BaseModel):
    start_data: date
    end_data: Optional[date] = None
    grup: Optional[FlagGrupLabel] = FlagGrupLabel.ZONE

    @field_validator("end_data")
    def check_dates(cls, end_data, info):
        start_data = info.data.get("start_data")
        if end_data is None:
            end_data = start_data
        if end_data < start_data:
            raise ValueError("data final menor que data inicial")
        return end_data


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
