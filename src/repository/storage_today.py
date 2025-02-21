# -*- coding: utf-8 -*-
from typing import List
from uuid import UUID
from datetime import datetime, date, timedelta
from sqlalchemy import func
from src.database import DBConnectionHandler, EventCountTemp, Camera, Filial
from src.dto import (
    ResponseTotalCountGrupZone,
    ResponseTotalCountGrupHour,
    ResponseTotalCountGrupCamera,
)


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

    def count_by_filial_count_grup_zone(
        self, filial_id: int
    ) -> List[ResponseTotalCountGrupZone]:
        with DBConnectionHandler() as session:
            try:
                counts = (
                    session.query(
                        func.sum(EventCountTemp.count_in).label("total_count_in"),
                        func.sum(EventCountTemp.count_out).label("total_count_out"),
                        Camera.tag,
                        Camera.tag.label("zone_name"),
                    )
                    .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                    .join(Filial, Camera.filial_id == Filial.filial_id)
                    .filter(Filial.filial_id == filial_id)
                    .group_by(Camera.tag)
                    .all()
                )
                return [
                    ResponseTotalCountGrupZone(
                        zone_name=count.zone_name,
                        total_count_in=count.total_count_in,
                        total_count_out=count.total_count_out,
                    )
                    for count in counts
                ]
            except Exception as error:
                session.rollback()
                raise error

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
