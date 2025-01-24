# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import (
    RequestEventCount,
    ResponseEventCount,
    ResponseTotalCount,
    ResponseTotalCountGrupZone,
    ResponseTotalCountGrupHour,
    ResponseTotalCountGrupCamera,
)


class InterfaceStorageTodayService(ABC):
    @abstractmethod
    def get_count_by_filial(self, filial_id: int) -> ResponseTotalCount:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_count_grup_zone(
        self, filial_id: int
    ) -> List[ResponseTotalCountGrupZone]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_grup_hour(
        self, filial_id: int
    ) -> List[ResponseTotalCountGrupHour]:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_camera_grup_hour(
        self, filial_id: int
    ) -> List[ResponseTotalCountGrupCamera]:
        raise NotImplementedError("Method no implemented")
