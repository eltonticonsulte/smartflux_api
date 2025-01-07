# -*- coding: utf-8 -*-
import logging
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from src.database import DBConnectionHandler
from src.database import (
    EventCountTemp,
    EventCount,
    Zone,
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
                    Zone.zone_id,
                    Zone.name.label("zone_name"),
                    Filial.filial_id,
                )
                .join(Camera, EventCountTemp.channel_id == Camera.channel_id)
                .join(Zone, Camera.zona_id == Zone.zone_id)
                .join(Filial, Zone.filial_id == Filial.filial_id)
                .group_by(
                    Camera.channel_id,
                    func.date_trunc("hour", EventCountTemp.event_time),
                    Zone.zone_id,
                    Zone.name,
                    Filial.filial_id,
                )
                .all()
            )
            return aggregated_data
