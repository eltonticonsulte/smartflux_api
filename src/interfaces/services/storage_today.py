# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from src.dto import (
    ResponseTotalCount,
    ResponseGrupData,
)


class InterfaceStorageTodayService(ABC):
    @abstractmethod
    def get_count_by_filial(self, filial_id: int) -> ResponseTotalCount:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_grup_zone(self, filial_id: int) -> ResponseGrupData:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_zone_grup_hour(
        self, filial_id: int, name_zona: str
    ) -> ResponseGrupData:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_camera_grup_hour(
        self, filial_id: int, name_device: str
    ) -> ResponseGrupData:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_grup_hour(self, filial_id: int) -> ResponseGrupData:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_grup_camera(self, filial_id: int) -> ResponseGrupData:
        raise NotImplementedError("Method no implemented")
