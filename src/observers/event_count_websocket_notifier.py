# -*- coding: utf-8 -*-
from fastapi.websockets import WebSocket
from src.interfaces import InterfaceObserver


class DataEventWebSocketNotifier(InterfaceObserver):
    def __init__(self):
        self.connections = {}

    async def add_connection(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.connections[client_id] = websocket

    async def remove_connection(self, client_id: str):
        if client_id in self.connections:
            await self.connections[client_id].close()
            del self.connections[client_id]

    async def update(self, client_id: str, event_data: dict) -> None:
        websocket = self.connections.get(client_id)
        if websocket:
            await websocket.send_json(event_data)
