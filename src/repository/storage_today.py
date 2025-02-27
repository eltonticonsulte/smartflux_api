# -*- coding: utf-8 -*-
from typing import Any, List, Tuple
from uuid import UUID
from datetime import datetime, date, timedelta
from sqlalchemy import func, Row
from src.database import DBConnectionHandler, EventCountTemp, Camera, Filial
from src.dto import (
    ResponseTotalCountGrupCamera,
)
from src.enums.storage import FlagGrupDate


class RepositoryCountEventException(Exception):
    def __init__(self, message):
        super().__init__(message)


class StorageTodayRepository:
    def count_by_filial(self, filial_id: int) -> List[Row[Tuple[int, int]]]:
        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCountTemp.count_in).label("total_count_in"),
                    func.sum(EventCountTemp.count_out).label("total_count_out"),
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .filter(Filial.filial_id == filial_id)
                .one()
            )
            return counts

    def count_by_filial_grup_zone(
        self, filial_id: int
    ) -> List[Row[Tuple[int, int, str, str]]]:
        with DBConnectionHandler() as session:

            counts = (
                session.query(
                    func.sum(EventCountTemp.count_in).label("total_count_in"),
                    func.sum(EventCountTemp.count_out).label("total_count_out"),
                    Camera.tag,
                    Camera.tag.label("label"),
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .filter(Filial.filial_id == filial_id)
                .group_by(Camera.tag)
                .all()
            )
            return counts

    def count_by_filial_grup_camera(
        self, filial_id: int
    ) -> List[Row[Tuple[int, int, str, str]]]:
        with DBConnectionHandler() as session:

            counts = (
                session.query(
                    func.sum(EventCountTemp.count_in).label("total_count_in"),
                    func.sum(EventCountTemp.count_out).label("total_count_out"),
                    Camera.name,
                    Camera.name.label("label"),
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .filter(Filial.filial_id == filial_id)
                .group_by(Camera.channel_id)
                .all()
            )
            return counts

    def count_by_filial_grup_hour(
        self, filial_id: int, date: date = date.today()
    ) -> List[dict]:
        start_date = datetime.combine(date, datetime.min.time())
        end_date = start_date + timedelta(days=1)
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
                    .join(Filial, Camera.filial_id == Filial.filial_id)
                    .filter(Filial.filial_id == filial_id)
                    .filter(EventCountTemp.event_time.between(start_date, end_date))
                    .group_by(func.date_trunc("hour", EventCountTemp.event_time))
                    .order_by("hour_timestamp")
                    .all()
                )
                return counts
            except Exception as error:
                session.rollback()
                raise error

    def count_by_filial_zone_grup_hour(
        self, filial_id: int, name_zona: str, date: date = date.today()
    ):
        start_date = datetime.combine(date, datetime.min.time())
        end_date = start_date + timedelta(days=1)
        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCountTemp.count_in).label("total_count_in"),
                    func.sum(EventCountTemp.count_out).label("total_count_out"),
                    func.date_trunc("hour", EventCountTemp.event_time).label(
                        "hour_timestamp"
                    ),
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .filter(Camera.tag == name_zona)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .filter(Filial.filial_id == filial_id)
                .filter(EventCountTemp.event_time.between(start_date, end_date))
                .group_by(func.date_trunc("hour", EventCountTemp.event_time))
                .order_by("hour_timestamp")
                .all()
            )
            return counts

    def count_by_filial_camera_grup_hour(
        self, filial_id: int, name_device: str, date: date = date.today()
    ):
        start_date = datetime.combine(date, datetime.min.time())
        end_date = start_date + timedelta(days=1)
        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCountTemp.count_in).label("total_count_in"),
                    func.sum(EventCountTemp.count_out).label("total_count_out"),
                    func.date_trunc("hour", EventCountTemp.event_time).label(
                        "hour_timestamp"
                    ),
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .filter(Camera.name == name_device)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .filter(Filial.filial_id == filial_id)
                .filter(EventCountTemp.event_time.between(start_date, end_date))
                .group_by(func.date_trunc("hour", EventCountTemp.event_time))
                .order_by("hour_timestamp")
                .all()
            )

            return counts

    def xget_count_by_filial_camera_grup_date(
        self,
        filial_id: int,
        start_date: date,
        end_date: date,
        name_camera: str,
        flag_time: FlagGrupDate,
    ) -> List[Row[Tuple[int, int, Any]]]:

        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCountTemp.count_in).label("total_count_in"),
                    func.sum(EventCountTemp.count_out).label("total_count_out"),
                    func.date_trunc(
                        flag_time.value.lower(), EventCountTemp.event_time
                    ).label("timestamp"),
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .filter(Camera.name == name_camera)
                .filter(Filial.filial_id == filial_id)
                # .filter(EventCountTemp.event_time.between(start_day, end_day))
                .group_by(
                    func.date_trunc(
                        flag_time.value.lower(), EventCountTemp.event_time
                    ).label("timestamp")
                )
                .order_by("timestamp")
                .all()
            )

            return counts

    def xget_count_by_filial_zone_grup_date(
        self,
        filial_id: int,
        start_date: date,
        end_date: date,
        zone: str,
        flag_time: FlagGrupDate,
    ) -> List[Row[Tuple[int, int, Any]]]:

        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCountTemp.count_in).label("total_count_in"),
                    func.sum(EventCountTemp.count_out).label("total_count_out"),
                    func.date_trunc(
                        flag_time.value.lower(), EventCountTemp.event_time
                    ).label("timestamp"),
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .filter(Camera.tag == zone)
                .filter(Filial.filial_id == filial_id)
                # .filter(EventCountTemp.event_time.between(start_day, end_day))
                .group_by(
                    func.date_trunc(
                        flag_time.value.lower(), EventCountTemp.event_time
                    ).label("timestamp")
                )
                .order_by("timestamp")
                .all()
            )

            return counts

    def xget_count_by_filial_grup_date(
        self,
        filial_id: int,
        start_date: date,
        end_date: date,
        flag_time: FlagGrupDate,
    ) -> List[Row[Tuple[int, int, Any]]]:

        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCountTemp.count_in).label("total_count_in"),
                    func.sum(EventCountTemp.count_out).label("total_count_out"),
                    func.date_trunc(
                        flag_time.value.lower(), EventCountTemp.event_time
                    ).label("timestamp"),
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .filter(Filial.filial_id == filial_id)
                # .filter(EventCountTemp.event_time.between(start_day, end_day))
                .group_by(
                    func.date_trunc(
                        flag_time.value.lower(), EventCountTemp.event_time
                    ).label("timestamp")
                )
                .order_by("timestamp")
                .all()
            )

            return counts

    def nnget_count_by_filial_grup_zone_date(
        self, filial_id: int, start_date: date, end_date: date, grup: FlagGrupDate
    ):
        min_time = datetime.combine(start_date, datetime.min.time())
        max_time = datetime.combine(end_date, datetime.max.time())
        str_time = grup.value.lower()
        with DBConnectionHandler() as session:
            counts = (
                session.query(
                    func.sum(EventCountTemp.count_in).label("total_count_in"),
                    func.sum(EventCountTemp.count_out).label("total_count_out"),
                    Camera.tag.label("label"),
                    func.date_trunc(str_time, EventCountTemp.event_time).label(
                        "hour_timestamp"
                    ),
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .filter(Filial.filial_id == filial_id)
                .filter(EventCountTemp.event_time.between(min_time, max_time))
                .group_by(
                    func.date_trunc(str_time, EventCountTemp.event_time), Camera.tag
                )
                .order_by("hour_timestamp")
                .all()
            )

            return counts

    def delete_by_channel_ids(self, channel_ids: List[UUID]):
        with DBConnectionHandler() as session:
            try:
                session.query(EventCountTemp).filter(
                    EventCountTemp.channel_id.in_(channel_ids)
                ).delete()
                session.commit()
            except Exception as error:
                session.rollback()
                raise error
