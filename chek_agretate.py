# -*- coding: utf-8 -*-
import time
from sqlalchemy import func
from src.database import DBConnectionHandler
from src.database import EventCount  # Substitua pelo caminho correto do modelo

with DBConnectionHandler() as session:
    # Construindo a consulta
    query = (
        session.query(
            EventCount.channel_id,
            EventCount.date,
            EventCount.hour,
            func.count().label("row_count"),
        )
        .group_by(EventCount.channel_id, EventCount.date, EventCount.hour)
        .order_by(EventCount.date, EventCount.channel_id, EventCount.hour)
    )

    # Executando a consulta
    start = time.time()
    result = query.all()
    end = time.time()
    print("timer", end - start)

    # Exibindo os resultados
    for row in result:
        if row.row_count > 1:
            print(
                f"error, Channel ID: {row.channel_id}, Date: {row.date}, Hour: {row.hour}, Row Count: {row.row_count}"
            )
    #    print(f"Channel ID: {row.channel_id}, Date: {row.date}, Hour: {row.hour}, Row Count: {row.row_count}")
