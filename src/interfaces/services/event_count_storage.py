# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from datetime import date
from src.dto import TotalCountGrupZone, TotalCountGroupDay


class InterfaceStorageService(ABC):
    @abstractmethod
    def get_count_by_filial_count_grup_zone(
        self, filial_id: int, current_date: date
    ) -> TotalCountGrupZone:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_grup_zone_periodo(
        self, filial_id: int, start_day: date, end_day: date
    ) -> List[TotalCountGrupZone]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_group_day(
        self, filial_id: int, year: int, month: int
    ) -> List[TotalCountGroupDay]:
        raise NotImplementedError("Method not implemented")
