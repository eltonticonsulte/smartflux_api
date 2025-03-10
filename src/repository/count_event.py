# -*- coding: utf-8 -*-
from typing import List
from uuid import UUID
from sqlalchemy import func
from src.database import DBConnectionHandler, EventCountTemp


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
