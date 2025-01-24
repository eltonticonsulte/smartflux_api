# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import RequestEventCount


class InterfaceObserver(ABC):
    @abstractmethod
    async def update(self, data: List[RequestEventCount], filial_id: int) -> None:
        raise NotImplementedError("Method not implemented")
