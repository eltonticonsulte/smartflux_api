# -*- coding: utf-8 -*-
from typing import List
from src.dto import EventCountRequest
from src.repository import CountEventRepository
from src.mappers import CountEventMapper
from .base_observer import InterfaceObserver


class DataEventCountSave(InterfaceObserver):
    def __init__(self, repository: CountEventRepository):
        self.repository = repository

    def update(self, data: List[EventCountRequest], filial_id: int) -> None:
        result = [CountEventMapper.create_event_request_to_entity(data)]
        self.repository.create_all(result)
