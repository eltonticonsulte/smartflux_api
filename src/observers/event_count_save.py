# -*- coding: utf-8 -*-
from typing import List
from src.dto import EventCountRequest
from src.repository import CountEventRepository
from src.mappers import CountEventMapper
from src.interfaces import InterfaceObserver


class DataEventCountSave(InterfaceObserver):
    def __init__(self, repository: CountEventRepository):
        self.repository = repository

    def update(self, datas: List[EventCountRequest], filial_id: int) -> None:
        result = [
            CountEventMapper.create_event_request_to_entity(data) for data in datas
        ]
        self.repository.create_all(result)
