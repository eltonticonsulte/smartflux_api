# -*- coding: utf-8 -*-
from typing import List, Tuple, Any
from datetime import date, datetime, timedelta
from sqlalchemy import func, Row
from src.database import DBConnectionHandler, EventCount, Camera, Filial
from src.dto import ResponseTotalCountGrupZone
from src.enums import DataFilterTimer


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

    def get_count_by_filial_grup_zone_date(
        self, filial_id: int, current_date: date, flag_time: DataFilterTimer
    ) -> List[Row[Tuple[int, int, int, str]]]:
        start_date = datetime.combine(current_date, datetime.min.time())
        end_date = start_date + timedelta(days=1)
        flag_time_value = flag_time.value.lower()

        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    Camera.tag.label("label"),
                    func.date_trunc(flag_time_value, EventCount.timestamp).label(
                        "timestamp"
                    ),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(EventCount.date.between(start_date, end_date))
                .group_by(flag_time_value, Camera.tag)
                .all()
            )
            return counts

    def get_count_by_filial_grup_cameras_date(
        self, filial_id: int, current_date: date, flag_time: DataFilterTimer
    ) -> List[Row[Tuple[int, int, int, str]]]:
        start_date = datetime.combine(current_date, datetime.min.time())
        end_date = start_date + timedelta(days=1)
        flag_time_value = flag_time.value.lower()

        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    Camera.name.label("label"),
                    func.date_trunc(flag_time_value, EventCount.timestamp).label(
                        "timestamp"
                    ),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(EventCount.date.between(start_date, end_date))
                .group_by(flag_time_value, Camera.channel_id)
                .all()
            )
            return counts

    def get_count_by_filial_grup_date(
        self, filial_id: int, start_day: date, end_day: date, flag_time: DataFilterTimer
    ) -> List[Row[Tuple[int, int, Any]]]:

        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    func.date_trunc(
                        flag_time.value.lower(), EventCount.timestamp
                    ).label("timestamp"),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(EventCount.date.between(start_day, end_day))
                .group_by(
                    func.date_trunc(flag_time.value.lower(), EventCount.timestamp)
                )
                .order_by("timestamp")
                .all()
            )

            return counts
