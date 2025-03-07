# -*- coding: utf-8 -*-
from typing import List, Tuple
from uuid import UUID
from datetime import date
from sqlalchemy import func, Row
from src.database import (
    DBConnectionHandler,
    EventCountTemp,
    WebsocketNotification,
    Camera,
    Filial,
    CountMaximunCapacity,
)


class CountEventRepository:
    def create_all(self, events: List[EventCountTemp]):
        with DBConnectionHandler() as session:
            try:
                session.bulk_save_objects(events)
                session.commit()
            except Exception as error:
                session.rollback()
                raise error

    def create(self, event: EventCountTemp):
        with DBConnectionHandler() as session:
            session.add(event)
            session.commit()
            return event.count_event_id

    def register_websocket(self, event: WebsocketNotification):
        with DBConnectionHandler() as session:
            session.add(event)
            session.commit()

    def get_by_token(self, token: UUID) -> Filial:
        with DBConnectionHandler() as session:

            filial = session.query(Filial).filter(Filial.token_api == token).first()
            return filial

    def get_max_capacity(self, filial_id: int) -> CountMaximunCapacity:
        with DBConnectionHandler() as session:
            capacity = (
                session.query(CountMaximunCapacity)
                .filter(
                    CountMaximunCapacity.filial_id == filial_id,
                    CountMaximunCapacity.date == date.today(),
                )
                .first()
            )
            return capacity

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

    def delete_by_channel_ids(self, channel_ids: List[UUID]):
        with DBConnectionHandler() as session:
            session.query(EventCountTemp).filter(
                EventCountTemp.channel_id.in_(channel_ids)
            ).delete()
            session.commit()
