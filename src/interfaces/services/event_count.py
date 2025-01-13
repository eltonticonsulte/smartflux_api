# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from src.dto import (
    EventCountRequest,
    EventCountResponse,
    TotalCount,
    TotalCountGrupZone,
    TotalCountGrupHour,
)


class InterfaceEventCountService(ABC):
    @abstractmethod
    def insert_pull(
        self, request: List[EventCountRequest], channels: List[UUID]
    ) -> List[EventCountResponse]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_filial_by_user_id(self, filial_id: int) -> int:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial(self, filial_id: int) -> TotalCount:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_count_grup_zone(
        self, filial_id: int
    ) -> List[TotalCountGrupZone]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_grup_hour(self, filial_id: int) -> List[TotalCountGrupHour]:
        raise NotImplementedError("Method not implemented")
