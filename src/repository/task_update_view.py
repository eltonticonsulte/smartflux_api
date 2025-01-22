# -*- coding: utf-8 -*-
import logging
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from src.database import DBConnectionHandler
from src.database import (
    EventCountTemp,
    EventCount,
    Filial,
    Camera,
)  # Importar as classes definidas


class TaskUpdateViewRepository:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def fetch_aggregate(self):
        with DBConnectionHandler() as session:
            aggregated_data = (
                session.query(
                    Camera.channel_id,
                    func.date_trunc("hour", EventCountTemp.event_time).label(
                        "hour_timestamp"
                    ),
                    func.sum(EventCountTemp.count_in).label("total_count_in"),
                    func.sum(EventCountTemp.count_out).label("total_count_out"),
                    Filial.filial_id,
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .join(Filial, Camera.filial_id == Filial.filial_id)
                .group_by(
                    Camera.channel_id,
                    func.date_trunc("hour", EventCountTemp.event_time),
                    Filial.filial_id,
                )
                .all()
            )
            return aggregated_data
