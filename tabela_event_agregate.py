# -*- coding: utf-8 -*-
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


def aggregate_events():
    with DBConnectionHandler() as session:
        # Query para agrupar os eventos por hora, filial, e zona
        print("len event ", session.query(EventCountTemp).count())
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
            # .filter(EventCountTemp.event_time >= data_inicio, EventCountTemp.event_time < data_fim)
            .group_by(
                Camera.channel_id,
                func.date_trunc("hour", EventCountTemp.event_time),
                Zone.zone_id,
                Zone.name,
                Filial.filial_id,
            )
            .all()
        )
        print("aggregated_data", len(aggregated_data))

        # Inserir dados agregados na tabela EventCount
        for data in aggregated_data:
            new_event_count = EventCount(
                channel_id=data.channel_id,
                date=data.hour_timestamp.date(),
                hour=data.hour_timestamp.hour,
                total_count_in=data.total_count_in,
                total_count_out=data.total_count_out,
                filial_id=data.filial_id,
                zona_id=data.zone_id,
                zone_name=data.zone_name,
            )
            session.add(new_event_count)

        # Commit das mudanças
        session.commit()

        # Remover dados processados de EventCountTemp
        # session.query(EventCountTemp).delete()
        # session.commit()

        print("Dados agregados e removidos com sucesso!")


if __name__ == "__main__":
    aggregate_events()
