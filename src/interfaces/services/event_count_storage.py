# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from datetime import date
from src.dto import (
    ResponseGrupData,
    ResponseGrupDataLabel,
    RequestVisitorDate,
    RequestVisitorLabel,
    ResponseTotalCount,
)


class InterfaceStorageService(ABC):
    @abstractmethod
    def get_count_by_filial_grup_zone(
        self, filial_id: int, current_date: date
    ) -> ResponseGrupDataLabel:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_date(
        self, filial_id: int, date: date
    ) -> ResponseTotalCount:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def process_data_day(self):
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_grup_periodo(
        self, filial_id: int, start_day: date, end_day: date
    ) -> ResponseGrupData:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_visitor(
        self, filial_id: int, data: RequestVisitorDate
    ) -> ResponseGrupData:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_visitor_label(
        self, filial_id: int, data: RequestVisitorLabel
    ) -> ResponseGrupDataLabel:
        raise NotImplementedError("Method not implemented")
