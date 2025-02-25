# -*- coding: utf-8 -*-
import logging
from datetime import date
from src.interfaces import InterfaceStorageService
from src.dto import (
    ResponseTotalCountGrupZone,
    CountGrupData,
    LineGraph,
    ResponseGrupData,
    ResponseGrupDataCode,
    RequestVisitor,
)
from src.enums import DataFilterTimer
from src.repository import StorageRepository
from src.mappers import MapperStorage


class StorageServices(InterfaceStorageService):
    def __init__(self, repository: StorageRepository):
        self.log = logging.getLogger(__name__)
        self.repository = repository

    def get_count_by_filial_grup_zone(
        self, filial_id: int, current_date: date
    ) -> ResponseGrupDataCode:
        result = self.repository.get_count_by_filial_grup_zone(filial_id, current_date)
        return MapperStorage.to_response_grup_data_code(result)

    def get_count_by_filial_grup_periodo(
        self, filial_id: int, start_day: date, end_day: date
    ) -> ResponseGrupData:
        if (end_day - start_day).days < 1:
            self.log.info(f"agrupando por hora {start_day} {end_day}")
            result = self.repository.get_count_by_filial_grup_date(
                filial_id, start_day, end_day
            )
            return MapperStorage.to_response_grup_data_label(result)
            label = []
            count_in = []
            count_out = []
            lis_gup_hour = []
            for item in result:
                label.append(item.timestamp.strftime("%Y-%m-%d %H:%M"))
                count_in.append(item.total_count_in)
                count_out.append(item.total_count_out)
                lis_gup_hour.append(
                    CountGrupData(
                        people_in=item.total_count_in,
                        people_out=item.total_count_out,
                        hour=item.timestamp.strftime("%Y-%m-%d %H:%M"),
                    )
                )
            line = LineGraph(label=label, people_in=count_in, people_out=count_out)
            return ResponseGrupData(table=lis_gup_hour, linegraph=line)

        result = self.repository.get_count_by_filial_grup_day(
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
                CountGrupData(
                    people_in=item.total_count_in,
                    people_out=item.total_count_out,
                    hour=item.timestamp.strftime("%Y-%m-%d %H:%M"),
                )
            )
        line = LineGraph(label=label, people_in=count_in, people_out=count_out)
        return ResponseGrupData(table=lis_gup_hour, linegraph=line)

    def get_count_visitor(
        self, filial_id: int, data: RequestVisitor
    ) -> ResponseGrupData:

        if data.end_data is None:
            data.end_data = data.start_data
        data = self.compute_grup(data)

        if data.zone:
            return self.filter_by_zone(filial_id, data)
        if data.device:
            return self.filter_by_device(filial_id, data)
        return self.filter_by_date(filial_id, data)

    def filter_by_zone(self, filial_id, data: RequestVisitor) -> ResponseGrupData:
        result = self.repository.get_count_by_filial_grup_zone_date(
            filial_id=filial_id, current_date=data.start_data, flag_time=data.grup
        )
        if data.grup == DataFilterTimer.HOUR:
            return MapperStorage.to_response_grup_hour(result)
        if data.grup == DataFilterTimer.DAY:
            return MapperStorage.to_respone_grup_day(result)

    def filter_by_device(
        self, filial_id: int, data: RequestVisitor
    ) -> ResponseGrupData:
        result = self.repository.get_count_by_filial_grup_cameras_date(
            filial_id, data.start_data, data.grup
        )
        if data.grup == DataFilterTimer.HOUR:
            return MapperStorage.to_response_grup_hour(result)
        if data.grup == DataFilterTimer.DAY:
            return MapperStorage.to_respone_grup_day(result)

    def filter_by_date(self, filial_id: int, data: RequestVisitor) -> ResponseGrupData:
        result = self.repository.get_count_by_filial_grup_date(
            filial_id, data.start_data, data.end_data, data.grup
        )
        if data.grup == DataFilterTimer.HOUR:
            return MapperStorage.to_response_grup_hour(result)
        if data.grup == DataFilterTimer.DAY:
            return MapperStorage.to_respone_grup_day(result)

    def compute_grup(self, data: RequestVisitor):
        if data.grup == DataFilterTimer.UNDEFINED:
            self.log.warning(f"agrupamento não encontrado")
            if (data.start_data - data.end_data).days < 1:
                self.log.warning(
                    f"agrupando por hora {data.start_data} {data.end_data}"
                )
                data.grup = DataFilterTimer.HOUR
            else:
                self.log.warning(f"agrupando por dia {data.start_data} {data.end_data}")
                data.grup = DataFilterTimer.DAY
        return data
