# -*- coding: utf-8 -*-
import logging
from datetime import date
from src.interfaces import InterfaceVisitorService
from src.dto import (
    ResponseGrupData,
    ResponseGrupDataLabel,
    RequestVisitorDate,
    RequestVisitorLabel,
    ResponseTotalCount,
    RequestVisitorGrupDate,
)
from src.enums import FlagGrupDate, FlagGrupLabel
from src.repository import StorageRepository, StorageTodayRepository, CapacityRepository
from src.mappers import MapperVisitor


class VisitorServices(InterfaceVisitorService):
    def __init__(
        self,
        rep_storage: StorageRepository,
        rep_today: StorageTodayRepository,
        rep_capacity: CapacityRepository,
    ):
        self.log = logging.getLogger(__name__)
        self.rep_storage = rep_storage
        self.rep_storage_today = rep_today
        self.rep_capacity = rep_capacity

    def get_count_visitor_report(
        self, filial_id: int, data: RequestVisitorGrupDate
    ) -> str:
        data = self.compute_grup_zone(data)
        return self.get_count_by_filial_grup_zone_date(filial_id, data)

    def get_count_by_filial_grup_zone_date(
        self, filial_id: int, data: RequestVisitorDate
    ) -> str:
        if data.start_date == date.today() and data.end_date == date.today():
            result = self.rep_storage_today.get_count_by_filial_grup_zone_date(
                filial_id, data.start_date, data.end_date, data.grup
            )
            return MapperVisitor.merge_report_data(result, data.grup)

        result = self.rep_storage.get_count_by_filial_grup_zone_date(
            filial_id, data.start_date, data.end_date, data.grup
        )

        if data.start_date == date.today() or data.end_date == date.today():
            result_today = self.rep_storage_today.get_count_by_filial_grup_zone_date(
                filial_id, data.start_date, data.end_date, data.grup
            )
            result.extend(result_today)

        return MapperVisitor.merge_report_data(result, data.grup)

    def get_count_by_filial_date(
        self, filial_id: int, date_time: date
    ) -> ResponseTotalCount:
        if date_time == date_time.today():
            resul_count = self.rep_storage_today.count_by_filial(filial_id)
            return MapperVisitor.to_response_total_count(resul_count)
        reult = self.rep_storage.count_by_filial_date(filial_id, date_time)
        capacity = self.rep_capacity.get_count_by_filial_id(filial_id, date_time)
        return MapperVisitor.to_response_total_count(reult, capacity)

    def get_count_visitor_label(
        self, filial_id: int, data: RequestVisitorLabel
    ) -> ResponseGrupDataLabel:
        if data.end_date is None:
            data.end_date = data.start_date

        if data.end_date < data.start_date:
            raise Exception("data final menor que data inicial")

        if data.grup == FlagGrupLabel.ZONE:
            return self.get_count_grup_zone(filial_id, data)
        elif data.grup == FlagGrupLabel.CAMERA:
            return self.get_count_grup_camera(filial_id, data)

        raise Exception("grup invalido")

    def get_count_grup_zone(
        self, filial_id: int, data: RequestVisitorLabel
    ) -> ResponseGrupDataLabel:
        if data.end_date == date.today() and data.start_date == date.today():
            resul_count = self.rep_storage_today.count_by_filial_grup_zone(filial_id)
            return MapperVisitor.count_grup_label(resul_count)

        result = self.rep_storage.get_count_by_filial_grup_zone(
            filial_id, data.start_date, data.end_date
        )
        if data.start_date == date.today() or data.end_date == date.today():
            resul_count = self.rep_storage_today.count_by_filial_grup_zone(filial_id)
            result.extend(resul_count)
            return MapperVisitor.count_grup_label(result)
        return MapperVisitor.count_grup_label(result)

    def get_count_grup_camera(
        self, filial_id: int, data: RequestVisitorLabel
    ) -> ResponseGrupDataLabel:
        result = self.rep_storage.get_count_by_filial_grup_camera(
            filial_id, data.start_date, data.end_date
        )
        if data.start_date == date.today() or data.end_date == date.today():
            resul_count = self.rep_storage_today.count_by_filial_grup_camera(filial_id)
            result.extend(resul_count)
            return MapperVisitor.count_grup_label(result)
        return MapperVisitor.count_grup_label(result)

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
            start_date=data.start_date,
            end_date=data.end_date,
            zone=data.zone,
            flag_time=data.grup,
        )
        if data.start_date == date.today() or data.end_date == date.today():
            today_result = self.rep_storage_today.get_count_by_filial_zone_grup_date(
                filial_id=filial_id,
                start_date=data.start_date,
                end_date=data.end_date,
                zone=data.zone,
                flag_time=data.grup,
            )
            result.extend(today_result)
        return MapperVisitor.count_grup_date(result, data.grup)

    def filter_by_camera(
        self, filial_id: int, data: RequestVisitorDate
    ) -> ResponseGrupData:
        if data.start_date == date.today() and data.end_date == date.today():
            result = self.rep_storage_today.get_count_by_filial_camera_grup_date(
                filial_id, data.start_date, data.end_date, data.device, data.grup
            )
            return MapperVisitor.count_grup_date(result, data.grup)

        result = self.rep_storage.get_count_by_filial_camera_grup_date(
            filial_id, data.start_date, data.end_date, data.device, data.grup
        )
        if data.start_date == date.today() or data.end_date == date.today():
            today_result = self.rep_storage_today.get_count_by_filial_camera_grup_date(
                filial_id, data.start_date, data.end_date, data.device, data.grup
            )
            result.extend(today_result)

        return MapperVisitor.count_grup_date(result, data.grup)

    def filter_by_date(
        self, filial_id: int, data: RequestVisitorDate
    ) -> ResponseGrupData:
        if data.start_date == date.today() and data.end_date == date.today():
            result = self.rep_storage_today.get_count_by_filial_grup_date(
                filial_id, data.start_date, data.end_date, data.grup
            )
            return MapperVisitor.count_grup_date(result, data.grup)

        result = self.rep_storage.get_count_by_filial_grup_date(
            filial_id, data.start_date, data.end_date, data.grup
        )

        if data.start_date == date.today() or data.end_date == date.today():
            today_result = self.rep_storage_today.get_count_by_filial_grup_date(
                filial_id, data.start_date, data.end_date, data.grup
            )
            result.extend(today_result)

        return MapperVisitor.count_grup_date(result, data.grup)

    def compute_grup(self, data: RequestVisitorDate):
        if data.grup == FlagGrupDate.AUTO_SELECT:
            period = data.end_date - data.start_date
            self.log.warning(f"agrupamento não encontrado periodo {period.days} day")
            if period.days < 1:
                self.log.warning(
                    f"agrupando por hora {data.start_date} {data.end_date}"
                )
                data.grup = FlagGrupDate.HOUR
            else:
                self.log.warning(f"agrupando por dia {data.start_date} {data.end_date}")
                data.grup = FlagGrupDate.DAY
        return data

    def compute_grup_zone(self, data: RequestVisitorGrupDate):
        if data.grup == FlagGrupDate.AUTO_SELECT:
            period = data.end_date - data.start_date
            self.log.warning(f"agrupamento não encontrado periodo {period.days} day")
            if period.days < 1:
                self.log.warning(
                    f"agrupando por hora {data.start_date} {data.end_date}"
                )
                data.grup = FlagGrupDate.HOUR
            else:
                self.log.warning(f"agrupando por dia {data.start_date} {data.end_date}")
                data.grup = FlagGrupDate.DAY
        return data
