# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import RequestEventCount, UserPermissionAccessDTO, ResponseEventCount


class InterfaceEventService(ABC):
    @abstractmethod
    async def process_events(
        self, event: List[RequestEventCount], user: UserPermissionAccessDTO
    ) -> None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create_event(self, event: RequestEventCount) -> ResponseEventCount:
        raise NotImplementedError("Method not implemented")
