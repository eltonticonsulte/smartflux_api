# -*- coding: utf-8 -*-
from logging import getLogger
from datetime import date
from src.database import DBConnectionHandler, CountMaximunCapacity


class CapacityRepository:
    def __init__(self):
        self.log = getLogger(__name__)

    def update(self, capacity: CountMaximunCapacity):
        with DBConnectionHandler() as session:
            existing_capacity = (
                session.query(CountMaximunCapacity)
                .filter(
                    CountMaximunCapacity.filial_id == capacity.filial_id,
                    CountMaximunCapacity.date == date.today(),
                )
                .first()
            )
            if not existing_capacity:
                session.add(capacity)
                session.commit()
                return

            if capacity.count_maximun > existing_capacity.count_maximun:
                capacity.id = existing_capacity.id
                session.merge(capacity)
                session.commit()

    def get_count_by_filial_id(self, filial_id: int, date_time: date):
        with DBConnectionHandler() as session:
            result = (
                session.query(CountMaximunCapacity.count_maximun)
                .filter(
                    CountMaximunCapacity.filial_id == filial_id
                    and CountMaximunCapacity.date == date_time
                )
                .first()
            )
            if result is None:
                return 0
            return result[0]
