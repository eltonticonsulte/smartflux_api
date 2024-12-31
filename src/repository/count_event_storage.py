# -*- coding: utf-8 -*-
from sqlalchemy import func
from typing import List
from datetime import date
from ..database import (
    DBConnectionHandler,
    EventCountTemp,
    Camera,
    Zone,
    Filial,
    EventCount,
)
from .base_repository import BaseRepository
from ..dto import TotalCountGrupZone


class RepositoryCountEventStorageException(Exception):
    def __init__(self, message):
        super().__init__(message)


class CountEventStorageRepository(BaseRepository):
    def __init__(self):
        pass

    def get_count_by_filial_count_grup_zone(
        self, filial_id: int, date: date
    ) -> List[TotalCountGrupZone]:
        with DBConnectionHandler() as db:
            try:
                counts = (
                    db.query(
                        func.sum(EventCount.total_count_in).label("total_count_in"),
                        func.sum(EventCount.total_count_out).label("total_count_out"),
                        EventCount.zone_name,
                    )
                    .filter(EventCount.filial_id == filial_id)
                    .filter(EventCount.date == date)
                    .group_by(EventCount.zona_id, EventCount.zone_name)
                    .all()
                )
                return [
                    TotalCountGrupZone(
                        zone_name=count.zone_name,
                        total_count_in=count.total_count_in,
                        total_count_out=count.total_count_out,
                    )
                    for count in counts
                ]
            except Exception as error:
                db.rollback()
                raise error
