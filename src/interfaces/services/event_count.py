# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import EventCountRequest, UserPermissionAccessDTO, EventCountResponse


class InterfaceEventService(ABC):
    @abstractmethod
    async def process_events(
        self, event: List[EventCountRequest], user: UserPermissionAccessDTO
    ) -> None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_event(self, event: EventCountRequest) -> EventCountResponse:
        raise NotImplementedError("Method not implemented")
