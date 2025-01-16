# -*- coding: utf-8 -*-
from logging import getLogger
from typing import List
from fastapi import WebSocket
from src.interfaces import InterfaceObserver
from src.dto import EventCountRequest


class DataEventWebSocketNotifier(InterfaceObserver):
    def __init__(self):
        self.log = getLogger("DataEventWebSocketNotifier")
        self.log.info(" start get_stactic_count_event_websocket")
        self.connections = {}

    async def add_connection(self, websocket: WebSocket, client_id: int):
        self.connections[str(client_id)] = websocket
        self.log.debug(f"add_connection {client_id}")

    async def remove_connection(self, filial_id: int):
        if filial_id in self.connections:
            await self.connections[str(filial_id)].close()
            del self.connections[str(filial_id)]

    async def update(self, datas: List[EventCountRequest], filial_id: int) -> None:
        self.log.debug(f"update {datas} {filial_id}")
        websocket = self.connections.get(str(filial_id))
        if websocket is None:
            self.log.error(f"WebSocket not found for client ID: {filial_id}")
            return
        try:
            for data in datas:
                await websocket.send_json(data.to_dict())
        except Exception as error:
            self.log.error(f"Erro ao enviar mensagem para o WebSocket: {error}")
            self.remove_connection(str(filial_id))
