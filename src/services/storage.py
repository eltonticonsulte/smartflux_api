# -*- coding: utf-8 -*-
import logging
from typing import List
from datetime import date
from src.interfaces import InterfaceStorageService
from src.dto import (
    ResponseTotalCountGrupZone,
    ResponseTotalCountGroupDay,
    CountGrup,
    LineGraph,
    ResponseGrupData,
)
from src.repository import StorageRepository
from src.mappers import MapperStorage


class StorageServices(InterfaceStorageService):
    def __init__(self, repository: StorageRepository):
        self.log = logging.getLogger(__name__)
        self.repository = repository

    def get_count_by_filial_grup_zone(
        self, filial_id: int, current_date: date
    ) -> ResponseGrupData:
        result = self.repository.get_count_by_filial_grup_zone(filial_id, current_date)
        return MapperStorage.to_response_grup_data(result)

    def get_count_by_filial_grup_periodo(
        self, filial_id: int, start_day: date, end_day: date
    ) -> List[ResponseTotalCountGrupZone]:
        if (end_day - start_day).days < 1:
            self.log.info(f"agrupando por hora {start_day} {end_day}")
            result = self.repository.get_count_by_filial_grup_hour(
                filial_id, start_day, end_day
            )
            label = []
            count_in = []
            count_out = []
            lis_gup_hour = []
            for item in result:
                label.append(item.timestamp.strftime("%Y-%m-%d %H:%M"))
                count_in.append(item.total_count_in)
                count_out.append(item.total_count_out)
                lis_gup_hour.append(
                    CountGrup(
                        people_in=item.total_count_in,
                        people_out=item.total_count_out,
                        hour=item.timestamp.strftime("%Y-%m-%d %H:%M"),
                    )
                )
            line = LineGraph(label=label, people_int=count_in, people_out=count_out)
            return ResponseGrupData(table=lis_gup_hour, linegraph=line)

        result = self.repository.get_count_by_filial_grup_periodo(
            filial_id, start_day, end_day
        )
        label = []
        count_in = []
        count_out = []
        lis_gup_hour = []
        for item in result:
            label.append(item.timestamp.strftime("%Y-%m-%d %H:%M"))
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            lis_gup_hour.append(
                CountGrup(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    hour=item.timestamp.strftime("%Y-%m-%d %H:%M"),
                )
            )
        line = LineGraph(label=label, people_int=count_in, people_out=count_out)
        return ResponseGrupData(table=lis_gup_hour, linegraph=line)

    def get_count_by_filial_group_day(
        self, filial_id: int, year: int, month: int
    ) -> List[ResponseTotalCountGroupDay]:
        return self.repository.get_filial_month_group_day(filial_id, year, month)
