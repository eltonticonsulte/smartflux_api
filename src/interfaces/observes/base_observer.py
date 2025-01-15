# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import EventCountRequest


class InterfaceObserver(ABC):
    @abstractmethod
    def update(self, data: List[EventCountRequest], filial_id: int) -> None:
        raise NotImplementedError("Method not implemented")
