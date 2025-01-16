# -*- coding: utf-8 -*-
from typing import List
from datetime import date
from sqlalchemy import func
from src.database import DBConnectionHandler, EventCount, Camera, Zone, Filial
from src.dto import TotalCountGrupZone, TotalCountGroupDay


class RepositoryCountEventStorageException(Exception):
    def __init__(self, message):
        super().__init__(message)


class StorageRepository:
    def __init__(self):
        pass

    def create_all(self, events: List[EventCount]):
        with DBConnectionHandler() as session:
            try:
                session.bulk_save_objects(events)
                session.commit()
            except Exception as error:
                session.rollback()
                raise error

    def get_count_by_filial_count_grup_zone(
        self, filial_id: int, current_date: date
    ) -> List[TotalCountGrupZone]:
        with DBConnectionHandler() as session:
            try:
                counts = (
                    session.query(
                        func.sum(EventCount.total_count_in).label("total_count_in"),
                        func.sum(EventCount.total_count_out).label("total_count_out"),
                        EventCount.zone_name,
                    )
                    .filter(EventCount.filial_id == filial_id)
                    .filter(EventCount.date == current_date)
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
                session.rollback()
                raise error

    def get_count_by_filial_grup_zone_periodo(
        self, filial_id: int, start_day: date, end_day: date
    ) -> List[TotalCountGrupZone]:
        with DBConnectionHandler() as session:
            try:
                result = (
                    session.query(
                        func.sum(EventCount.total_count_in).label("total_count_in"),
                        func.sum(EventCount.total_count_out).label("total_count_out"),
                        EventCount.zone_name,
                    )
                    .filter(EventCount.filial_id == filial_id)
                    .filter(EventCount.date > start_day)
                    .group_by(EventCount.zona_id, EventCount.zone_name)
                    .all()
                )
                return [
                    TotalCountGrupZone(
                        zone_name=count.zone_name,
                        total_count_in=count.total_count_in,
                        total_count_out=count.total_count_out,
                    )
                    for count in result
                ]
            except Exception as error:
                session.rollback()
                raise error

    def get_filial_month_group_day(
        self, filial_id: int, year: int, month: int
    ) -> List[TotalCountGroupDay]:
        with DBConnectionHandler() as session:
            try:
                counts = (
                    session.query(
                        func.sum(EventCount.total_count_in).label("total_count_in"),
                        func.sum(EventCount.total_count_out).label("total_count_out"),
                        EventCount.date.label("day"),
                    )
                    .filter(EventCount.filial_id == filial_id)
                    .filter(func.extract("year", EventCount.date) == year)
                    .filter(func.extract("month", EventCount.date) == month)
                    .group_by(EventCount.date)
                    .order_by(EventCount.date)
                    .all()
                )
                return [
                    TotalCountGroupDay(
                        day=count.day.strftime("%Y-%m-%d"),
                        total_count_in=count.total_count_in,
                        total_count_out=count.total_count_out,
                    )
                    for count in counts
                ]
            except Exception as error:
                session.rollback()
                raise error
