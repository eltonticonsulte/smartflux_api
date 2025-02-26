# -*- coding: utf-8 -*-
from typing import List, Tuple, Any
from sqlalchemy import Row
from src.enums import DataFilterTimer
from src.dto import (
    ResponseGrupData,
    CountGrupData,
    LineGraph,
    ResponseGrupDataLabel,
    CountGrupCode,
)


class MapperStorage:
    @staticmethod
    def to_response_grup_label(
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
                    date=item.label,
                )
            )
        line = LineGraph(label=label, people_in=count_in, people_out=count_out)
        return ResponseGrupData(table=lis_gup_hour, linegraph=line)

    @staticmethod
    def merge_data(
        counts: List[Row[Tuple[int, int, Any]]],
        counts2: List[Row[Tuple[int, int, Any]]],
        flag_time: DataFilterTimer,
    ) -> ResponseGrupData:
        str_format_time = (
            "%Y-%m-%d %H:%M" if flag_time == DataFilterTimer.HOUR else "%Y-%m-%d"
        )

        labels = []
        count_in = []
        count_out = []
        list_gup_data = []
        for item in counts:
            label = item.timestamp.strftime(str_format_time)
            labels.append(label)
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            list_gup_data.append(
                CountGrupData(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    date=label,
                )
            )
        for item in counts2:
            label = item.timestamp.strftime(str_format_time)
            labels.append(label)
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            list_gup_data.append(
                CountGrupData(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    date=label,
                )
            )

        line = LineGraph(label=labels, people_in=count_in, people_out=count_out)
        return ResponseGrupData(table=list_gup_data, linegraph=line)

    @staticmethod
    def merge_data_label(
        counts: List[Row[Tuple[int, int, Any]]],
        counts2: List[Row[Tuple[int, int, Any]]],
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
        for item in counts2:
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
    def to_response_grup_date(
        counts: List[Row[Tuple[int, int, Any]]], flag_time: DataFilterTimer
    ) -> ResponseGrupData:
        str_format_time = (
            "%Y-%m-%d %H:%M" if flag_time == DataFilterTimer.HOUR else "%Y-%m-%d"
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
                CountGrupData(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    date=item.timestamp.strftime(str_format_time),
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
        return ResponseGrupDataLabel(table=lis_gup_code, linegraph=line)
