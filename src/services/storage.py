# -*- coding: utf-8 -*-
import logging
from datetime import date
from ..interfaces import InterfaceStorageService
from ..dto import TotalCountGrupZone
from ..repository import StorageRepository


class StorageServices(InterfaceStorageService):
    def __init__(self, repository: StorageRepository):
        self.log = logging.getLogger(__name__)
        self.repository = repository

    def get_count_by_filial_count_grup_zone(
        self, filial_id: int, current_date: date
    ) -> TotalCountGrupZone:
        return self.repository.get_count_by_filial_count_grup_zone(
            filial_id, current_date
        )
