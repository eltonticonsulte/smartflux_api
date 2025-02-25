# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from datetime import date
from src.dto import ResponseGrupData, ResponseGrupDataCode, RequestVisitor


class InterfaceStorageService(ABC):
    @abstractmethod
    def get_count_by_filial_grup_zone(
        self, filial_id: int, current_date: date
    ) -> ResponseGrupDataCode:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_by_filial_grup_periodo(
        self, filial_id: int, start_day: date, end_day: date
    ) -> ResponseGrupData:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_count_visitor(
        self, filial_id: int, data: RequestVisitor
    ) -> ResponseGrupData:
        raise NotImplementedError("Method not implemented")
