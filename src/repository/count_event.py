# -*- coding: utf-8 -*-
from typing import List
from sqlalchemy import func
from ..database import DBConnectionHandler, EventCountTemp, Camera, Zone, Filial
from .base_repository import BaseRepository
from ..dto import TotalCount


class RepositoryCountEventException(Exception):
    def __init__(self, message):
        super().__init__(message)


class CountEventRepository(BaseRepository):
    def __init__(self):
        pass

    def create_all(self, events: List[EventCountTemp]):
        with DBConnectionHandler() as db:
            try:
                db.bulk_save_objects(events)
                db.commit()
            except Exception as error:
                db.rollback()
                raise error

    def count_by_filial(self, filial_id: int) -> TotalCount:
        with DBConnectionHandler() as db:
            try:
                count = (
                    db.query(
                        func.count(EventCountTemp.count_in).label("total_count_in"),
                        func.count(EventCountTemp.count_out).label("total_count_out"),
                    )
                    .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                    .join(Zone, Camera.zona_id == Zone.zone_id)
                    .join(Filial, Zone.filial_id == Filial.filial_id)
                    .one()
                )
                return TotalCount(
                    total_count_in=count.total_count_in,
                    total_count_out=count.total_count_out,
                )
            except Exception as error:
                db.rollback()
                raise error
