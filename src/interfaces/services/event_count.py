# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from fastapi import WebSocket
from src.dto import EventCountRequest, UserPermissionAccessDTO


class InterfaceEventService(ABC):
    @abstractmethod
    async def process_event(
        self, event: List[EventCountRequest], user: UserPermissionAccessDTO
    ) -> None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def add_websocket_connection(
        self, websocket: WebSocket, filial_id: int
    ) -> None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def remove_websocket_connection(self, filial_id: int) -> None:
        raise NotImplementedError("Method not implemented")
