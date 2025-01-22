# -*- coding: utf-8 -*-
from typing import List
from uuid import UUID
from datetime import datetime
from sqlalchemy import func
from src.database import DBConnectionHandler, EventCountTemp, Camera, Filial
from src.dto import TotalCountGrupZone, TotalCountGrupHour, TotalCountGrupCamera


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
    ) -> List[TotalCountGrupZone]:
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

    def get_count_by_camera_grup_hour(
        self, filial_id: int
    ) -> List[TotalCountGrupCamera]:
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
                    TotalCountGrupCamera(
                        camera=count.camera,
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
                    .join(Filial, Camera.filial_id == Filial.filial_id)
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
