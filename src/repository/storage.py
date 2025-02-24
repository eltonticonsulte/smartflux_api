# -*- coding: utf-8 -*-
from typing import List, Tuple, Any
from datetime import date, datetime, timedelta
from sqlalchemy import func, Row
from src.database import DBConnectionHandler, EventCount, Camera, Filial
from src.dto import ResponseTotalCountGrupZone, ResponseTotalCountGroupDay


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

    def get_count_by_filial_grup_zone(
        self, filial_id: int, current_date: date
    ) -> List[Row[Tuple[int, int, int, str]]]:

        start_date = datetime.combine(current_date, datetime.min.time())
        end_date = start_date + timedelta(days=1)

        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    Camera.tag.label("label"),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(EventCount.date.between(start_date, end_date))
                .group_by(Camera.filial_id, Camera.tag)
                .all()
            )
            return counts

    def get_count_by_filial_grup_zone_periodo(
        self, filial_id: int, start_day: date, end_day: date
    ) -> List[ResponseTotalCountGrupZone]:
        with DBConnectionHandler() as session:
            try:
                result = (
                    session.query(
                        func.sum(EventCount.total_count_in).label("total_count_in"),
                        func.sum(EventCount.total_count_out).label("total_count_out"),
                        Camera.tag.label("camera_tag"),
                    )
                    .join(Camera, Camera.channel_id == EventCount.channel_id)
                    .filter(EventCount.filial_id == filial_id)
                    .filter(EventCount.date > start_day)
                    .group_by(Camera.tag)
                    .all()
                )
                return [
                    ResponseTotalCountGrupZone(
                        zone_name=count.camera_tag,
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
    ) -> List[ResponseTotalCountGroupDay]:
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
                    ResponseTotalCountGroupDay(
                        day=count.day.strftime("%Y-%m-%d"),
                        total_count_in=count.total_count_in,
                        total_count_out=count.total_count_out,
                    )
                    for count in counts
                ]
            except Exception as error:
                session.rollback()
                raise error

    # o agrupamento deve ser por dia
    def get_count_by_filial_grup_periodo(
        self, filial_id: int, start_day: date, end_day: date
    ) -> List[Row[Tuple[int, int, Any]]]:
        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    func.date_trunc("day", EventCount.date).label("timestamp"),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(EventCount.date.between(start_day, end_day))
                .group_by(func.date_trunc("day", EventCount.date))
                .order_by("timestamp")
                .all()
            )
            return counts

    def get_count_by_filial_grup_hour(
        self, filial_id: int, start_day: date, end_day: date
    ) -> List[Row[Tuple[int, int, Any]]]:
        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    func.date_trunc("hour", EventCount.date).label("timestamp"),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(EventCount.date.between(start_day, end_day))
                .group_by(func.date_trunc("hour", EventCount.date))
                .order_by("timestamp")
                .all()
            )
            return counts
