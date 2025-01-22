# -*- coding: utf-8 -*-
from logging import getLogger
from typing import Optional, List
from src.repository import WebSocketRepository
from src.dto import (
    UserPermissionAccessDTO,
    EventCountSendWebsocket,
    EventCountDataValidate,
)
from src.interfaces import InterfaceUserService
from src.external import DataEventWebSocketNotifier
from src.mappers import CountEventMapper


class WebSocketNotifierService:
    def __init__(
        self,
        repo: WebSocketRepository,
        service_user: InterfaceUserService,
        external_websocket: DataEventWebSocketNotifier,
    ):
        self.log = getLogger(__name__)
        self.repo = repo
        self.service_user = service_user
        self.external_websocket = external_websocket

    async def process_websocket(
        self, datas: List[EventCountDataValidate], filial_id: int
    ):
        connect_id = self.get_ref_websocket_connect(filial_id)
        self.log.debug(f"connect_id {connect_id}")
        if not connect_id:
            self.log.warning(f"Cannot user connect_id filial {filial_id}")
            return
        for data in datas:
            data_ws = CountEventMapper.create_event_validate_to_websocket(data)
            await self.external_websocket.update(data_ws, connect_id)

    def get_ref_websocket_connect(self, filial_id: int) -> Optional[str]:
        datas = self.repo.fetch_all()
        for data in datas:
            connect_id = data.connect_id
            try:
                user: UserPermissionAccessDTO = self.service_user.current_user(
                    data.token_filial
                )
                if user.filial_id == filial_id:
                    return connect_id
            except Exception as error:
                self.log.error(f"Erro ao obter usuário: {error}")
                continue
