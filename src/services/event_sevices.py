# -*- coding: utf-8 -*-
from typing import List
import logging
import uuid
from src.interfaces import InterfaceEventService
from src.observers import SubjectEventCount
from src.repository import CountEventRepository, CameraRepository
from src.database import EventCountTemp
from src.observers.event_count_websocket_notifier import DataEventWebSocketNotifier
from src.dto import EventCountRequest, UserPermissionAccessDTO, EventCountResponse
from src.mappers import CountEventMapper


class EventService(InterfaceEventService):
    def __init__(
        self,
        camera_repository: CameraRepository,
        observer: SubjectEventCount,
    ):
        self.log = logging.getLogger(__name__)
        self.subject = observer
        self.camera_repository = camera_repository

    async def process_event(
        self, event: List[EventCountRequest], user: UserPermissionAccessDTO
    ) -> None:
        cameras = self.camera_repository.get_by_filial(user.filial_id)
        channels = [camera.channel_id for camera in cameras]
        data_success, data_fail = self.check_chennel(event, channels)
        result: List[EventCountResponse] = []
        if data_success:
            entity_data: List[EventCountTemp] = [
                CountEventMapper.create_event_request_to_entity(data)
                for data in data_success
            ]
            await self.subject.notify_observers(data_success, user.filial_id)

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
                    description=f"Channel not found in current filial {user.filial_id} {data.channel_id}",
                )
            )

        return result

    async def add_websocket_connection(self, websocket, filial_id):
        data_notifi: DataEventWebSocketNotifier = self.subject.find_data_websoket()
        if not data_notifi:
            self.log.warning(f"Cannot add wesocket connect ")
        await data_notifi.add_connection(websocket, filial_id)

    async def remove_websocket_connection(self, filial_id: int):
        data_notifi: DataEventWebSocketNotifier = self.subject.find_data_websoket()
        if data_notifi:
            await data_notifi.remove_connection(filial_id)

    def check_chennel(
        self, datas: List[EventCountRequest], channels: List[uuid.UUID]
    ) -> List[EventCountRequest]:
        datas_fail = []
        data_success = []

        for data in datas:
            if data.channel_id not in channels:
                self.log.error(f"Channel not found {data.channel_id} {channels}")
                datas_fail.append(data)
            else:
                data_success.append(data)
        return data_success, datas_fail
