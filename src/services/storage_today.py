# -*- coding: utf-8 -*-
from typing import List
import logging
from src.interfaces import InterfaceTodayStorageService
from src.dto import (
    TotalCount,
    TotalCountGrupZone,
    TotalCountGrupHour,
)
from src.repository import TodayEstorageRepository


class TodayStorageServices(InterfaceTodayStorageService):
    def __init__(self, repo: TodayEstorageRepository):
        self.log = logging.getLogger(__name__)
        self.repo = repo

    def get_count_by_filial(self, filial_id: int) -> TotalCount:
        data = self.repo.count_by_filial(filial_id)
        count_in = data.get("total_count_in", 0)
        count_out = data.get("total_count_out", 0)

        return TotalCount(
            total_count_in=count_in if count_in is not None else 0,
            total_count_out=count_out if count_out is not None else 0,
        )

    def get_count_by_filial_count_grup_zone(
        self, filial_id: int
    ) -> List[TotalCountGrupZone]:
        return self.repo.count_by_filial_count_grup_zone(filial_id)

    def get_count_by_filial_grup_hour(self, filial_id: int) -> List[TotalCountGrupHour]:
        return self.repo.count_by_filial_grup_hour(filial_id)
