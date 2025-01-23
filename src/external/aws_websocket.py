# -*- coding: utf-8 -*-
from logging import getLogger
import json
import boto3
from botocore.config import Config
from core import get_settings
from src.interfaces import InterfaceObserver
from src.dto import EventCountSendWebsocket


class DataEventWebSocketNotifier(InterfaceObserver):
    def __init__(self):
        self.log = getLogger("DataEventWebSocketNotifier")
        self.log.info(" start get_stactic_count_event_websocket")
        self.endpoint = get_settings().WEBSOCKET_ENDPOINT
        config = Config(
            retries={"max_attempts": 10, "mode": "standard"},
            connect_timeout=5,
            read_timeout=5,
        )
        # session = boto3.Session(profile_name="smartflux")
        self.client = boto3.client(
            "apigatewaymanagementapi",
            endpoint_url=self.endpoint,
            region_name=get_settings().AWS_REGION,
            config=config,
        )
        self.log.info(f" auth {self.client}")

    async def update(self, data: EventCountSendWebsocket, connection_id: str) -> None:

        try:
            response = self.client.post_to_connection(
                ConnectionId=connection_id, Data=json.dumps(data.to_dict())
            )
        except Exception as error:
            self.log.error(
                f"Erro ao enviar mensagem para o WebSocket: {error}", exc_info=error
            )
