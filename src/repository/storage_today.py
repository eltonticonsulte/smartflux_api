# -*- coding: utf-8 -*-
from typing import Any, List, Tuple
from uuid import UUID
from datetime import datetime, date, timedelta
from sqlalchemy import func, Row
from src.database import DBConnectionHandler, EventCountTemp, Camera, Filial
from src.dto import (
    ResponseTotalCountGrupZone,
    ResponseTotalCountGrupHour,
    ResponseTotalCountGrupCamera,
)
from src.enums.storage import DataFilterTimer


class RepositoryCountEventException(Exception):
    def __init__(self, message):
        super().__init__(message)


class StorageTodayRepository:
    def count_by_filial(self, filial_id: int) -> dict:
        with DBConnectionHandler() as session:
            try:
                count = (
                    session.query(
                        func.sum(EventCountTemp.count_in).label("total_count_in"),
                        func.sum(EventCountTemp.count_out).label("total_count_out"),
                    )
                    .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                    .join(Filial, Camera.filial_id == Filial.filial_id)
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

    def select_all_data_last_day(self) -> List[Row[Tuple[UUID, Any, int, int, int]]]:
        with DBConnectionHandler() as session:
            start_date = datetime.combine(
                date.today() - timedelta(days=1), datetime.max.time()
            )
            all_data = (
                session.query(
                    Camera.channel_id,
                    func.date_trunc("hour", EventCountTemp.event_time).label(
                        "hour_timestamp"
                    ),
                    func.sum(EventCountTemp.count_in).label("total_count_in"),
                    func.sum(EventCountTemp.count_out).label("total_count_out"),
                    Filial.filial_id,
                    func.array_agg(EventCountTemp.count_event_id).label(
                        "event_ids"
                    ),  # EventCountTemp.count_event_id
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .filter(EventCountTemp.event_time < start_date)
                .group_by(
                    Camera.channel_id,
                    func.date_trunc("hour", EventCountTemp.event_time),
                    Filial.filial_id,
                )
                .all()
            )
            return all_data

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

    def get_count_by_camera_grup_hour(
        self, filial_id: int
    ) -> List[ResponseTotalCountGrupCamera]:
        with DBConnectionHandler() as session:
            try:
                counts = (
                    session.query(
                        func.sum(EventCountTemp.count_in).label("total_count_in"),
                        func.sum(EventCountTemp.count_out).label("total_count_out"),
                        Camera.name.label("camera"),
                    )
                    .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                    .join(Filial, Camera.filial_id == Filial.filial_id)
                    .filter(Filial.filial_id == filial_id)
                    .group_by(Camera.channel_id, Camera.name)
                    .all()
                )
                return [
                    ResponseTotalCountGrupCamera(
                        camera=count.camera,
                        total_count_in=count.total_count_in,
                        total_count_out=count.total_count_out,
                    )
                    for count in counts
                ]
            except Exception as error:
                session.rollback()
                raise error

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
        flag_time: DataFilterTimer,
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
        flag_time: DataFilterTimer,
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
        flag_time: DataFilterTimer,
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

    def delete_by_event_ids(self, ids: List[int]):
        with DBConnectionHandler() as session:
            session.query(EventCountTemp).filter(
                EventCountTemp.count_event_id.in_(ids)
            ).delete(synchronize_session="fetch")

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
