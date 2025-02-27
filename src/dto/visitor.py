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


class ResponseVisitoBase(BaseModel):
    start_date: date
    end_date: Optional[date] = None

    @field_validator("end_date", mode="before")
    def check_dates(cls, end_date, info):
        start_data = info.data.get("start_date")
        if end_date is None:
            end_date = start_data
        if end_date < start_data:
            raise ValueError("data final menor que data inicial")
        return end_date


class RequestVisitorGrupDate(ResponseVisitoBase):
    grup: Optional[FlagGrupDate] = FlagGrupDate.AUTO_SELECT

    @field_validator("grup", mode="before")
    def check_grup(cls, grup, info):
        if grup != FlagGrupDate.AUTO_SELECT:
            return grup
        start_date = info.data.get("start_date")
        end_date = info.data.get("end_date")
        if end_date is None:
            raise ValueError("invalid date")
        print(start_date, end_date)
        period = end_date - start_date
        if period.days < 1:
            grup = FlagGrupDate.HOUR
        else:
            grup = FlagGrupDate.DAY
        return grup


class RequestVisitorDate(RequestVisitorGrupDate):
    zone: Optional[str] = None
    device: Optional[str] = None


class RequestVisitorLabel(ResponseVisitoBase):
    grup: Optional[FlagGrupLabel] = FlagGrupLabel.ZONE
