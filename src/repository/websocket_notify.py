# -*- coding: utf-8 -*-
from typing import List
from src.database import DBConnectionHandler, WebsocketNotification


class WebSocketRepository:
    def __init__(self):
        pass

    def fetch_all(self) -> List[WebsocketNotification]:
        with DBConnectionHandler() as db:
            return db.query(WebsocketNotification).all()

    def delete(self, connect_id: str) -> None:
        with DBConnectionHandler() as db:
            db.query(WebsocketNotification).filter(
                WebsocketNotification.connect_id == connect_id
            ).delete()
            db.commit()
