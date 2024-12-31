# -*- coding: utf-8 -*-
import logging
from datetime import date
from ..interfaces import InterfaceEventCountStorageService
from ..dto import EventCountRequest, EventCountResponse, TotalCountGrupZone
from ..mappers import CountEventMapper
from ..repository import CountEventStorageRepository


class CountEventStorageServices(InterfaceEventCountStorageService):
    def __init__(self, repository: CountEventStorageRepository):
        self.log = logging.getLogger(__name__)
        self.repository = repository

    def get_count_by_filial_count_grup_zone(
        self, filial_id: int, date: date
    ) -> TotalCountGrupZone:
        return self.repository.get_count_by_filial_count_grup_zone(filial_id, date)
