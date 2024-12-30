# -*- coding: utf-8 -*-
from typing import List
import uuid
import logging
from ..interfaces import InterfaceEventCountService
from ..dto import EventCountRequest, EventCountResponse
from ..mappers import CountEventMapper
from ..repository import CountEventRepository


class CountEventServices(InterfaceEventCountService):
    def __init__(self, repository: CountEventRepository):
        self.log = logging.getLogger(__name__)
        self.repository = repository

    def insert_pull(
        self, request: List[EventCountRequest], channels: List[uuid.UUID]
    ) -> List[EventCountResponse]:
        data_success, data_fail = self.check_chennel(request, channels)
        result: List[EventCountResponse] = []
        if data_success:
            entity_data = [
                CountEventMapper.create_event_request_to_entity(data)
                for data in data_success
            ]
            self.repository.add_all(entity_data)
        for data in data_success:
            result.append(
                EventCountResponse(
                    event_id=data.event_id, status=True, description="Success"
                )
            )

        for data in data_fail:
            result.append(
                EventCountResponse(
                    event_id=data.event_id,
                    status=False,
                    description="Channel not found in current filial",
                )
            )
        return result

    def check_chennel(
        self, datas: List[EventCountRequest], channels: List[uuid.UUID]
    ) -> List[EventCountRequest]:
        datas_fail = []
        data_success = []

        for data in datas:
            if data.channel_id not in channels:
                datas_fail.append(data)
            else:
                data_success.append(data)
        return data_success, datas_fail
