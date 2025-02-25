# -*- coding: utf-8 -*-
from typing import List, Tuple, Any
from sqlalchemy import Row
from src.dto import (
    ResponseGrupData,
    CountGrupData,
    LineGraph,
    ResponseGrupDataCode,
    CountGrupCode,
)


class MapperStorage:
    @staticmethod
    def to_response_grup_data_label(
        counts: List[Row[Tuple[int, int, Any]]]
    ) -> ResponseGrupData:
        label = []
        count_in = []
        count_out = []
        lis_gup_hour = []
        for item in counts:
            label.append(item.label)
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            lis_gup_hour.append(
                CountGrupData(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    hour=item.label,
                )
            )
        line = LineGraph(label=label, people_in=count_in, people_out=count_out)
        return ResponseGrupData(table=lis_gup_hour, linegraph=line)

    @staticmethod
    def to_response_grup_hour(
        counts: List[Row[Tuple[int, int, Any]]]
    ) -> ResponseGrupData:
        label = []
        count_in = []
        count_out = []
        lis_gup_hour = []
        for item in counts:
            label.append(item.timestamp.strftime("%Y-%m-%d %H:%M"))
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            lis_gup_hour.append(
                CountGrupData(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    date=item.timestamp.strftime("%Y-%m-%d %H:%M"),
                )
            )
        line = LineGraph(label=label, people_in=count_in, people_out=count_out)
        return ResponseGrupData(table=lis_gup_hour, linegraph=line)

    @staticmethod
    def to_respone_grup_day(
        counts: List[Row[Tuple[int, int, Any]]]
    ) -> ResponseGrupData:
        label = []
        count_in = []
        count_out = []
        lis_gup_day = []
        for item in counts:
            label.append(item.timestamp.strftime("%Y-%m-%d"))
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            lis_gup_day.append(
                CountGrupData(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    date=item.timestamp.strftime("%Y-%m-%d"),
                )
            )
        line = LineGraph(label=label, people_in=count_in, people_out=count_out)
        return ResponseGrupData(table=lis_gup_day, linegraph=line)

    @staticmethod
    def to_response_grup_data_code(
        counts: List[Row[Tuple[int, int, Any]]]
    ) -> ResponseGrupData:
        label = []
        count_in = []
        count_out = []
        lis_gup_code = []
        for item in counts:
            label.append(item.label)
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            lis_gup_code.append(
                CountGrupCode(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    code=item.label,
                )
            )
        line = LineGraph(label=label, people_in=count_in, people_out=count_out)
        return ResponseGrupDataCode(table=lis_gup_code, linegraph=line)
