# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import EventCountRequest, UserPermissionAccessDTO


class InterfaceEventService(ABC):
    @abstractmethod
    def process_event(
        self, event: List[EventCountRequest], user: UserPermissionAccessDTO
    ) -> None:
        raise NotImplementedError("Method not implemented")
