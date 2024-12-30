# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import EventCountRequest, EventCountResponse
from uuid import UUID


class InterfaceEventCountService(ABC):
    @abstractmethod
    def insert_pull(
        self, request: List[EventCountRequest], channels: List[UUID]
    ) -> List[EventCountResponse]:
        raise NotImplementedError("Method not implemented")
