# -*- coding: utf-8 -*-
import logging
from typing import List
from datetime import date
from src.interfaces import InterfaceStorageService
from src.dto import ResponseTotalCountGrupZone, ResponseTotalCountGroupDay
from src.repository import StorageRepository


class StorageServices(InterfaceStorageService):
    def __init__(self, repository: StorageRepository):
        self.log = logging.getLogger(__name__)
        self.repository = repository

    def get_count_by_filial_count_grup_zone(
        self, filial_id: int, current_date: date
    ) -> ResponseTotalCountGrupZone:
        return self.repository.get_count_by_filial_count_grup_zone(
            filial_id, current_date
        )

    def get_count_by_filial_grup_zone_periodo(
        self, filial_id: int, start_day: date, end_day: date
    ) -> List[ResponseTotalCountGrupZone]:
        return self.repository.get_count_by_filial_grup_zone_periodo(
            filial_id, start_day, end_day
        )

    def get_count_by_filial_group_day(
        self, filial_id: int, year: int, month: int
    ) -> List[ResponseTotalCountGroupDay]:
        return self.repository.get_filial_month_group_day(filial_id, year, month)
