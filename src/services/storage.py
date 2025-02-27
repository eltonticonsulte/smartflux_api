# -*- coding: utf-8 -*-
import logging
from datetime import date
from src.interfaces import InterfaceStorageService
from src.dto import (
    CountGrupData,
    LineGraph,
    ResponseGrupData,
    ResponseGrupDataLabel,
    RequestVisitorDate,
    RequestVisitorLabel,
    ResponseTotalCount,
    RequestVisitorGrupZone,
)
from src.enums import FlagGrupDate, FlagGrupLabel
from src.repository import StorageRepository, StorageTodayRepository
from src.mappers import MapperStorage


class StorageServices(InterfaceStorageService):
    def __init__(
        self, rep_storage: StorageRepository, rep_today: StorageTodayRepository
    ):
        self.log = logging.getLogger(__name__)
        self.rep_storage = rep_storage
        self.rep_storage_today = rep_today

    def get_count_visitor_report(
        self, filial_id: int, data: RequestVisitorGrupZone
    ) -> str:
        data = self.compute_grup_zone(data)
        return self.get_count_by_filial_grup_zone_date(filial_id, data)

    def get_count_by_filial_grup_zone_date(
        self, filial_id: int, data: RequestVisitorDate
    ) -> str:
        if data.start_data == date.today() and data.end_data == date.today():
            result = self.rep_storage_today.nnget_count_by_filial_grup_zone_date(
                filial_id, data.start_data, data.end_data, data.grup
            )
            return MapperStorage.merge_report_data(result, data.grup)

        result = self.rep_storage.get_count_by_filial_grup_zone_date(
            filial_id, data.start_data, data.end_data, data.grup
        )

        if data.start_data == date.today() or data.end_data == date.today():
            result_today = self.rep_storage_today.nnget_count_by_filial_grup_zone_date(
                filial_id, data.start_data, data.end_data, data.grup
            )
            result.extend(result_today)

        return MapperStorage.merge_report_data(result, data.grup)

    def get_count_by_filial_date(
        self, filial_id: int, date: date
    ) -> ResponseTotalCount:
        if date == date.today():
            resul_count = self.rep_storage_today.count_by_filial(filial_id)
            return MapperStorage.to_response_total_count(resul_count)
        reult = self.rep_storage.count_by_filial_date(filial_id, date)
        return MapperStorage.to_response_total_count(reult)

    def get_count_visitor_label(
        self, filial_id: int, data: RequestVisitorLabel
    ) -> ResponseGrupDataLabel:
        if data.end_data is None:
            data.end_data = data.start_data

        if data.end_data < data.start_data:
            raise Exception("data final menor que data inicial")

        if data.grup == FlagGrupLabel.ZONE:
            return self.get_count_grup_zone(filial_id, data)
        elif data.grup == FlagGrupLabel.CAMERA:
            return self.get_count_grup_camera(filial_id, data)
        else:
            raise Exception("grup invalido")

    def get_count_grup_zone(
        self, filial_id: int, data: RequestVisitorLabel
    ) -> ResponseGrupDataLabel:
        if data.end_data == date.today() and data.start_data == date.today():
            resul_count = self.rep_storage_today.count_by_filial_grup_zone(filial_id)
            return MapperStorage.merge_data_label(resul_count, [])

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
  
    def get_count_visitor(
        self, filial_id: int, data: RequestVisitorDate
    ) -> ResponseGrupData:

        data = self.compute_grup(data)

        if data.zone and data.device:
            raise Exception("zona e device nao podem ser informados ao mesmo tempo")

        if data.zone:
            return self.filter_by_zone(filial_id, data)
        if data.device:
            return self.filter_by_camera(filial_id, data)
        return self.filter_by_date(filial_id, data)

    def filter_by_zone(self, filial_id, data: RequestVisitorDate) -> ResponseGrupData:
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
        self, filial_id: int, data: RequestVisitorDate
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

    def filter_by_date(
        self, filial_id: int, data: RequestVisitorDate
    ) -> ResponseGrupData:
        result = self.rep_storage.get_count_by_filial_grup_date(
            filial_id, data.start_data, data.end_data, data.grup
        )

        if data.start_data == date.today() or data.end_data == date.today():
            today_result = self.rep_storage_today.xget_count_by_filial_grup_date(
                filial_id, data.start_data, data.end_data, data.grup
            )
            return MapperStorage.merge_data(result, today_result, data.grup)

        return MapperStorage.to_response_grup_date(result, data.grup)

    def compute_grup(self, data: RequestVisitorDate):
        if data.grup == FlagGrupDate.AUTO_SELECT:
            period = data.end_data - data.start_data
            self.log.warning(f"agrupamento não encontrado periodo {period.days} day")
            if period.days < 1:
                self.log.warning(
                    f"agrupando por hora {data.start_data} {data.end_data}"
                )
                data.grup = FlagGrupDate.HOUR
            else:
                self.log.warning(f"agrupando por dia {data.start_data} {data.end_data}")
                data.grup = FlagGrupDate.DAY
        return data

    def compute_grup_zone(self, data: RequestVisitorGrupZone):
        if data.grup == FlagGrupDate.AUTO_SELECT:
            period = data.end_data - data.start_data
            self.log.warning(f"agrupamento não encontrado periodo {period.days} day")
            if period.days < 1:
                self.log.warning(
                    f"agrupando por hora {data.start_data} {data.end_data}"
                )
                data.grup = FlagGrupDate.HOUR
            else:
                self.log.warning(f"agrupando por dia {data.start_data} {data.end_data}")
                data.grup = FlagGrupDate.DAY
        return data
