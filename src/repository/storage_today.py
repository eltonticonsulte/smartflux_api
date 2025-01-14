# -*- coding: utf-8 -*-
from typing import List
from datetime import datetime
from sqlalchemy import func
from src.database import DBConnectionHandler, EventCountTemp, Camera, Zone, Filial
from src.dto import TotalCountGrupZone, TotalCountGrupHour


class RepositoryCountEventException(Exception):
    def __init__(self, message):
        super().__init__(message)


class TodayEstorageRepository:
    def count_by_filial(self, filial_id: int) -> dict:
        with DBConnectionHandler() as session:
            try:
                count = (
                    session.query(
                        func.sum(EventCountTemp.count_in).label("total_count_in"),
                        func.sum(EventCountTemp.count_out).label("total_count_out"),
                    )
                    .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                    .join(Zone, Camera.zona_id == Zone.zone_id)
                    .join(Filial, Zone.filial_id == Filial.filial_id)
                    .filter(Filial.filial_id == filial_id)
                    .one()
                )
                return {
                    "total_count_in": count.total_count_in,
                    "total_count_out": count.total_count_out,
                }

            except Exception as error:
                session.rollback()
                raise error

    def count_by_filial_count_grup_zone(
        self, filial_id: int
    ) -> List[TotalCountGrupZone]:
        with DBConnectionHandler() as session:
            try:
                counts = (
                    session.query(
                        func.sum(EventCountTemp.count_in).label("total_count_in"),
                        func.sum(EventCountTemp.count_out).label("total_count_out"),
                        Zone.zone_id,
                        Zone.name.label("zone_name"),
                    )
                    .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                    .join(Zone, Camera.zona_id == Zone.zone_id)
                    .join(Filial, Zone.filial_id == Filial.filial_id)
                    .filter(Filial.filial_id == filial_id)
                    .group_by(Zone.zone_id, Zone.name)
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
                session.rollback()
                raise error

    def count_by_filial_grup_hour(self, filial_id: int) -> List[TotalCountGrupHour]:
        with DBConnectionHandler() as session:
            try:
                counts = (
                    session.query(
                        func.sum(EventCountTemp.count_in).label("total_count_in"),
                        func.sum(EventCountTemp.count_out).label("total_count_out"),
                        func.date_trunc("hour", EventCountTemp.event_time).label(
                            "hour_timestamp"
                        ),
                    )
                    .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                    .join(Zone, Camera.zona_id == Zone.zone_id)
                    .join(Filial, Zone.filial_id == Filial.filial_id)
                    .filter(Filial.filial_id == filial_id)
                    .group_by(func.date_trunc("hour", EventCountTemp.event_time))
                    .all()
                )
                return [
                    TotalCountGrupHour(
                        hour=datetime.strftime(count.hour_timestamp, "%H:%M"),
                        total_count_in=count.total_count_in,
                        total_count_out=count.total_count_out,
                    )
                    for count in counts
                ]
            except Exception as error:
                session.rollback()
                raise error
