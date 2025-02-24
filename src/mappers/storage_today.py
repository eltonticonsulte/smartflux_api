# -*- coding: utf-8 -*-
from typing import List, Tuple, Any
from sqlalchemy import Row
from src.dto import ResponseGrupDataHour, CountGrupHour, LineGraph


class MapperStorageToday:
    @staticmethod
    def to_response_grup_data(
        counts: List[Row[Tuple[int, int, Any]]]
    ) -> ResponseGrupDataHour:
        label = []
        count_in = []
        count_out = []
        lis_gup_hour = []
        for item in counts:
            label.append(item.label)
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            lis_gup_hour.append(
                CountGrupHour(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    hour=item.label,
                )
            )
        line = LineGraph(label=label, people_int=count_in, people_out=count_out)
        return ResponseGrupDataHour(table=lis_gup_hour, linegraph=line)
