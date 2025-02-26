# -*- coding: utf-8 -*-
import logging
from datetime import date
from src.interfaces import InterfaceStorageService
from src.dto import (
    ResponseTotalCountGrupZone,
    CountGrupData,
    LineGraph,
    ResponseGrupData,
    ResponseGrupDataLabel,
    RequestVisitor,
    RequestVisitorLabel,
)
from src.enums import DataFilterTimer, DataGrupLabel
from src.repository import StorageRepository, StorageTodayRepository
from src.mappers import MapperStorage


class StorageServices(InterfaceStorageService):
    def __init__(
        self, rep_storage: StorageRepository, rep_today: StorageTodayRepository
    ):
        self.log = logging.getLogger(__name__)
        self.rep_storage = rep_storage
        self.rep_storage_today = rep_today

    def get_count_visitor_label(
        self, filial_id: int, data: RequestVisitorLabel
    ) -> ResponseGrupDataLabel:
        if data.end_data is None:
            data.end_data = data.start_data

        if data.end_data < data.start_data:
            raise Exception("data final menor que data inicial")

        if data.grup == DataGrupLabel.ZONE:
            return self.get_count_grup_zone(filial_id, data)
        elif data.grup == DataGrupLabel.CAMERA:
            return self.get_count_grup_camera(filial_id, data)
        else:
            raise Exception("grup invalido")

    def get_count_grup_zone(
        self, filial_id: int, data: RequestVisitorLabel
    ) -> ResponseGrupDataLabel:
        result = self.rep_storage.get_count_by_filial_grup_zone(
            filial_id, data.start_data, data.end_data
        )
        if data.start_data == date.today() or data.end_data == date.today():
            resul_count = self.rep_storage_today.count_by_filial_grup_zone(filial_id)
            return MapperStorage.merge_data_label(result, resul_count)
        return MapperStorage.merge_data_label(result, [])

    def get_count_grup_camera(
        self, filial_id: int, data: RequestVisitorLabel
    ) -> ResponseGrupDataLabel:
        result = self.rep_storage.get_count_by_filial_grup_camera(
            filial_id, data.start_data, data.end_data
        )
        if data.start_data == date.today() or data.end_data == date.today():
            resul_count = self.rep_storage_today.count_by_filial_grup_camera(filial_id)
            return MapperStorage.merge_data_label(result, resul_count)
        return MapperStorage.merge_data_label(result, [])

    def get_count_by_filial_grup_zone(
        self, filial_id: int, current_date: date
    ) -> ResponseGrupDataLabel:
        result = self.rep_storage.get_count_by_filial_grup_zone(filial_id, current_date)
        return MapperStorage.to_response_grup_data_code(result)

    def get_count_by_filial_grup_periodo(
        self, filial_id: int, start_day: date, end_day: date
    ) -> ResponseGrupData:
        if (end_day - start_day).days < 1:
            self.log.info(f"agrupando por hora {start_day} {end_day}")
            result = self.rep_storage.get_count_by_filial_grup_date(
                filial_id, start_day, end_day
            )
            return MapperStorage.to_response_grup_label(result)
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

        result = self.rep_storage.get_count_by_filial_grup_day(
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
        if data.end_data < data.start_data:
            raise Exception("data final menor que data inicial")
        if data.zone and data.device:
            raise Exception("zona e device nao podem ser informados ao mesmo tempo")

        if data.zone:
            return self.filter_by_zone(filial_id, data)
        if data.device:
            return self.filter_by_camera(filial_id, data)
        return self.filter_by_date(filial_id, data)

    def filter_by_zone(self, filial_id, data: RequestVisitor) -> ResponseGrupData:
        result = self.rep_storage.get_count_by_filial_zone_grup_date(
            filial_id=filial_id,
            start_date=data.start_data,
            end_date=data.end_data,
            zone=data.zone,
            flag_time=data.grup,
        )
        if data.start_data == date.today() or data.end_data == date.today():
            today_result = self.rep_storage_today.xget_count_by_filial_zone_grup_date(
                filial_id=filial_id,
                start_date=data.start_data,
                end_date=data.end_data,
                zone=data.zone,
                flag_time=data.grup,
            )
            return MapperStorage.merge_data(result, today_result, data.grup)
        return MapperStorage.to_response_grup_date(result, data.grup)

    def filter_by_camera(
        self, filial_id: int, data: RequestVisitor
    ) -> ResponseGrupData:
        result = self.rep_storage.get_count_by_filial_camera_grup_date(
            filial_id, data.start_data, data.end_data, data.device, data.grup
        )
        if data.start_data == date.today() or data.end_data == date.today():
            today_result = self.rep_storage_today.xget_count_by_filial_camera_grup_date(
                filial_id, data.start_data, data.end_data, data.device, data.grup
            )
            return MapperStorage.merge_data(result, today_result, data.grup)
        return MapperStorage.to_response_grup_date(result, data.grup)

    def filter_by_date(self, filial_id: int, data: RequestVisitor) -> ResponseGrupData:
        result = self.rep_storage.get_count_by_filial_grup_date(
            filial_id, data.start_data, data.end_data, data.grup
        )

        if data.start_data == date.today() or data.end_data == date.today():
            today_result = self.rep_storage_today.xget_count_by_filial_grup_date(
                filial_id, data.start_data, data.end_data, data.grup
            )
            return MapperStorage.merge_data(result, today_result, data.grup)

        return MapperStorage.to_response_grup_date(result, data.grup)

    def compute_grup(self, data: RequestVisitor):
        if data.grup == DataFilterTimer.AUTO_SELECT:
            period = data.end_data - data.start_data
            self.log.warning(f"agrupamento não encontrado periodo {period.days} day")
            if period.days < 1:
                self.log.warning(
                    f"agrupando por hora {data.start_data} {data.end_data}"
                )
                data.grup = DataFilterTimer.HOUR
            else:
                self.log.warning(f"agrupando por dia {data.start_data} {data.end_data}")
                data.grup = DataFilterTimer.DAY
        return data
