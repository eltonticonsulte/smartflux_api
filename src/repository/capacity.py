# -*- coding: utf-8 -*-
from logging import getLogger
from src.database import DBConnectionHandler, CountMaximunCapacity


class CapacityRepository:
    def __init__(self):
        self.log = getLogger(__name__)

    def update(self, capacity: CountMaximunCapacity):
        with DBConnectionHandler() as session:
            existing_capacity = (
                session.query(CountMaximunCapacity)
                .filter(CountMaximunCapacity.filial_id == capacity.filial_id)
                .first()
            )
            if not existing_capacity:
                session.add(capacity)
                session.commit()
                return

            if capacity.count_maximun > existing_capacity.count_maximun:
                session.merge(capacity)
                session.commit()

    def get_count_by_filial_id(self, filial_id: int):
        with DBConnectionHandler() as session:
            return (
                session.query(CountMaximunCapacity.count_maximun)
                .filter(CountMaximunCapacity.filial_id == filial_id)
                .first()
            )
