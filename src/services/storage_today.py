# -*- coding: utf-8 -*-
import logging
from src.interfaces import InterfaceStorageTodayService
from src.mappers import MapperStorageToday
from src.dto import (
    ResponseTotalCount,
    ResponseTotalCountGrupCamera,
    ResponseGrupDataHour,
    CountGrupHour,
    LineGraph,
)
from src.repository import StorageTodayRepository


class StorageTodayServices(InterfaceStorageTodayService):
    def __init__(self, repo: StorageTodayRepository):
        self.log = logging.getLogger(__name__)
        self.repo = repo

    def get_count_by_filial(self, filial_id: int) -> ResponseTotalCount:
        data = self.repo.count_by_filial(filial_id)
        count_in = data.get("total_count_in", 0)
        count_out = data.get("total_count_out", 0)

        return ResponseTotalCount(
            total_count_in=count_in if count_in is not None else 0,
            total_count_out=count_out if count_out is not None else 0,
        )

    def get_count_by_filial_grup_zone(self, filial_id: int) -> ResponseGrupDataHour:
        result = self.repo.count_by_filial_grup_zone(filial_id)
        return MapperStorageToday.to_response_grup_data(result)

    def get_count_by_filial_grup_camera(self, filial_id: int) -> ResponseGrupDataHour:
        result = self.repo.count_by_filial_grup_camera(filial_id)
        return MapperStorageToday.to_response_grup_data(result)

    def get_count_by_filial_camera_grup_hour(
        self, filial_id: int, name_device: str
    ) -> ResponseGrupDataHour:
        result = self.repo.count_by_filial_camera_grup_hour(filial_id, name_device)
        self.log.critical(result)
        label = []
        count_in = []
        count_out = []
        lis_gup_hour = []

        for item in result:
            label.append(item.hour_timestamp.strftime("%Y-%m-%d %H:%M"))
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            lis_gup_hour.append(
                CountGrupHour(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    hour=item.hour_timestamp.strftime("%Y-%m-%d %H:%M"),
                )
            )

        line = LineGraph(label=label, people_int=count_in, people_out=count_out)
        return ResponseGrupDataHour(table=lis_gup_hour, linegraph=line)

    def get_count_by_filial_grup_hour(self, filial_id: int) -> ResponseGrupDataHour:
        result = self.repo.count_by_filial_grup_hour(filial_id)
        label = []
        count_in = []
        count_out = []
        lis_gup_hour = []

        for item in result:
            label.append(item.hour_timestamp.strftime("%Y-%m-%d %H:%M"))
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            lis_gup_hour.append(
                CountGrupHour(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    hour=item.hour_timestamp.strftime("%Y-%m-%d %H:%M"),
                )
            )

        line = LineGraph(label=label, people_int=count_in, people_out=count_out)
        return ResponseGrupDataHour(table=lis_gup_hour, linegraph=line)

    def get_count_by_filial_zone_grup_hour(
        self, filial_id: int, name_zona: str
    ) -> ResponseGrupDataHour:
        result = self.repo.count_by_filial_zone_grup_hour(filial_id, name_zona)
        label = []
        count_in = []
        count_out = []
        lis_gup_hour = []

        for item in result:
            label.append(item.hour_timestamp.strftime("%Y-%m-%d %H:%M"))
            count_in.append(item.total_count_in)
            count_out.append(item.total_count_out)
            lis_gup_hour.append(
                CountGrupHour(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    hour=item.hour_timestamp.strftime("%Y-%m-%d %H:%M"),
                )
            )

        line = LineGraph(label=label, people_int=count_in, people_out=count_out)
        return ResponseGrupDataHour(table=lis_gup_hour, linegraph=line)
