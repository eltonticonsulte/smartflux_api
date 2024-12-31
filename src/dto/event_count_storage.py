# -*- coding: utf-8 -*-
from pydantic import BaseModel


class TotalCountGrupZone(BaseModel):
    zone_name: str
    total_count_in: int
    total_count_out: int
