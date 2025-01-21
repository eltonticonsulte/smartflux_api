# -*- coding: utf-8 -*-
from logging import getLogger
import json
from typing import List
import boto3
from core import get_settings
from src.interfaces import InterfaceObserver
from src.dto import EventCountRequest


class DataEventWebSocketNotifier(InterfaceObserver):
    def __init__(self):
        self.log = getLogger("DataEventWebSocketNotifier")
        self.log.info(" start get_stactic_count_event_websocket")
        self.endpoint = get_settings().websocket_endpoint
        self.client = boto3.client(
            "apigatewaymanagementapi", endpoint_url=self.endpoint
        )
        self.connections: dict = {}

    def add_connection(self, connection_id: str, filial_id: int):
        self.log.debug(f"add_connection {connection_id}")
        self.connections[str(filial_id)] = connection_id

    async def update(self, datas: List[EventCountRequest], filial_id: int) -> None:
        self.log.debug(f"update {datas} {filial_id}")
        connection_id = self.connections.get(str(filial_id))

        try:
            for data in datas:
                response = self.client.post_to_connection(
                    ConnectionId=connection_id, Data=json.dumps(data.to_dict())
                )
        except Exception as error:
            self.log.error(f"Erro ao enviar mensagem para o WebSocket: {error}")
            self.remove_connection(str(filial_id))
