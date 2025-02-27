# -*- coding: utf-8 -*-
from typing import List, Tuple, Any
from sqlalchemy import Row
from src.enums import FlagGrupDate
from src.dto import (
    ResponseGrupData,
    CountGrupDate,
    LineGraph,
    ResponseGrupDataLabel,
    CountGrupCode,
    ResponseTotalCount,
)


class MapperStorage:
    @staticmethod
    def merge_report_data(
        counts: List[Row[Tuple[int, int, str, Any]]], flag_time: FlagGrupDate
    ):
        str_time_format = (
            "%Y-%m-%d %H:%M" if flag_time == FlagGrupDate.HOUR else "%Y-%m-%d"
        )
        header = "Zona,Data,Entrada,Saída\n"
        text_result = header
        for item in counts:
            line = f"{item.label},{item.hour_timestamp.strftime(str_time_format)},{item.total_count_in},{item.total_count_out}\n"
            text_result += line
        return text_result

    @staticmethod
    def count_grup_label(
        counts: List[Row[Tuple[int, int, Any]]],
    ) -> ResponseGrupData:

        labels = []
        count_in = []
        count_out = []
        list_gup_data = []
        for item in counts:

            labels.append(item.label)
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            list_gup_data.append(
                CountGrupCode(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    code=item.label,
                )
            )
        line = LineGraph(label=labels, people_in=count_in, people_out=count_out)
        return ResponseGrupDataLabel(table=list_gup_data, linegraph=line)

    @staticmethod
    def count_grup_date(
        counts: List[Row[Tuple[int, int, Any]]], flag_time: FlagGrupDate
    ) -> ResponseGrupData:
        str_format_time = (
            "%Y-%m-%d %H:%M" if flag_time == FlagGrupDate.HOUR else "%Y-%m-%d"
        )

        label = []
        count_in = []
        count_out = []
        lis_gup_hour = []
        for item in counts:
            label.append(item.timestamp.strftime(str_format_time))
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            lis_gup_hour.append(
                CountGrupDate(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    date=item.timestamp.strftime(str_format_time),
                )
            )
        line = LineGraph(label=label, people_in=count_in, people_out=count_out)
        return ResponseGrupData(table=lis_gup_hour, linegraph=line)

    @staticmethod
    def to_response_total_count(counts: List[Row[Tuple[int, int]]]) -> int:
        return ResponseTotalCount(
            total_count_in=counts.total_count_in,
            total_count_out=counts.total_count_out,
        )
