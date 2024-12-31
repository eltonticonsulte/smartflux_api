# -*- coding: utf-8 -*-
from typing import List
import uuid
import logging
from ..interfaces import InterfaceEventCountService
from ..dto import (
    EventCountRequest,
    EventCountResponse,
    TotalCount,
    TotalCountGrupZone,
    TotalCountGrupHour,
)
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
            self.repository.create_all(entity_data)
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

    def get_count_by_filial(self, filial_id: int) -> TotalCount:
        return self.repository.count_by_filial(filial_id)

    def get_count_by_filial_count_grup_zone(
        self, filial_id: int
    ) -> List[TotalCountGrupZone]:
        return self.repository.count_by_filial_count_grup_zone(filial_id)

    def get_count_by_filial_grup_hour(self, filial_id: int) -> List[TotalCountGrupHour]:
        return self.repository.count_by_filial_grup_hour(filial_id)
