# -*- coding: utf-8 -*-
from typing import List, Tuple, Any
from datetime import date, datetime
from sqlalchemy import func, Row
from src.database import DBConnectionHandler, EventCount, Camera, Filial
from src.dto import ResponseTotalCountGrupZone
from src.enums import FlagGrupDate


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

    def count_by_filial_date(self, filial_id: int, date: date) -> int:
        with DBConnectionHandler() as session:
            count = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(EventCount.date == date)
                .one()
            )
            return count

    def get_count_by_filial_grup_camera_date(
        self, filial_id: int, start_date: date, end_date: date
    ) -> List[Row[Tuple[int, int, int, str]]]:
        min_time = datetime.combine(start_date, datetime.min.time())
        max_time = datetime.combine(end_date, datetime.max.time())
        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    Camera.tag.label("label"),
                    func.date_trunc("hour", EventCount.timestamp).label(
                        "hour_timestamp"
                    ),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(EventCount.timestamp.between(min_time, max_time))
                .group_by(Camera.tag, func.date_trunc("hour", EventCount.timestamp))
                .all()
            )
            return counts

    def get_count_by_filial_grup_zone_date(
        self, filial_id: int, start_date: date, end_date: date
    ) -> List[Row[Tuple[int, int, int, str]]]:
        min_time = datetime.combine(start_date, datetime.min.time())
        max_time = datetime.combine(end_date, datetime.max.time())
        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    Camera.tag.label("label"),
                    func.date_trunc("hour", EventCount.timestamp).label(
                        "hour_timestamp"
                    ),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(EventCount.timestamp.between(min_time, max_time))
                .group_by(Camera.tag, func.date_trunc("hour", EventCount.timestamp))
                .all()
            )
            return counts

    def get_count_by_filial_grup_zone(
        self, filial_id: int, start_date: date, end_date: date
    ) -> List[Row[Tuple[int, int, int, str]]]:

        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    Camera.tag.label("label"),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(EventCount.date.between(start_date, end_date))
                .group_by(Camera.tag)
                .all()
            )
            return counts

    def get_count_by_filial_grup_camera(
        self, filial_id: int, start_date: date, end_date: date
    ) -> List[Row[Tuple[int, int, int, str]]]:

        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    Camera.name.label("label"),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(EventCount.date.between(start_date, end_date))
                .group_by(Camera.name)
                .all()
            )
            return counts

    def get_count_by_filial_zone_grup_date(
        self,
        filial_id: int,
        start_date: date,
        end_date: date,
        zone: str,
        flag_time: FlagGrupDate,
    ) -> List[Row[Tuple[int, int, int, str]]]:

        flag_time_value = flag_time.value.lower()

        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    func.date_trunc(flag_time_value, EventCount.timestamp).label(
                        "timestamp"
                    ),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(Camera.tag == zone)
                .filter(EventCount.date.between(start_date, end_date))
                .group_by(
                    func.date_trunc(flag_time_value, EventCount.timestamp).label(
                        "timestamp"
                    )
                )
                .order_by("timestamp")
                .all()
            )
            return counts

    def get_count_by_filial_camera_grup_date(
        self,
        filial_id: int,
        start_date: date,
        end_date: date,
        name_camera: str,
        flag_time: FlagGrupDate,
    ) -> List[Row[Tuple[int, int, int, str]]]:
        flag_time_value = flag_time.value.lower()

        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCount.total_count_in).label("total_count_in"),
                    func.sum(EventCount.total_count_out).label("total_count_out"),
                    func.date_trunc(flag_time_value, EventCount.timestamp).label(
                        "timestamp"
                    ),
                )
                .filter(EventCount.filial_id == filial_id)
                .filter(Camera.name == name_camera)
                .filter(EventCount.date.between(start_date, end_date))
                .group_by(
                    func.date_trunc(flag_time_value, EventCount.timestamp).label(
                        "timestamp"
                    )
                )
                .order_by("timestamp")
                .all()
            )
            return counts

    def get_count_by_filial_grup_date(
        self, filial_id: int, start_day: date, end_day: date, flag_time: FlagGrupDate
    ) -> List[Row[Tuple[int, int, Any]]]:
        str_timer = flag_time.value.lower()
        print(str_timer, start_day, end_day, filial_id)

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
