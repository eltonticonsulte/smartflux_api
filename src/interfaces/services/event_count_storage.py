# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from datetime import date
from src.dto import EventCountRequest, EventCountResponse, TotalCountGrupZone


class InterfaceEventCountStorageService(ABC):
    @abstractmethod
    def get_count_by_filial_count_grup_zone(
        self, filial_id: int, date: date
    ) -> TotalCountGrupZone:
        raise NotImplementedError("Method not implemented")
