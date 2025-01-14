# -*- coding: utf-8 -*-
from typing import List
import uuid
from src.interfaces import InterfaceEventService
from src.observers import SubjectEventCount
from src.repository import CountEventRepository, CameraRepository
from src.database import EventCountTemp
from src.observers.event_count_websocket_notifier import WebSocketNotifier
from src.dto import EventCountRequest, UserPermissionAccessDTO, EventCountResponse
from src.mappers import CountEventMapper


class EventService(InterfaceEventService):
    def __init__(
        self,
        repository: CountEventRepository,
        camera_repository: CameraRepository,
        observer: SubjectEventCount,
    ):
        self.subject = observer
        self.camera_repository = camera_repository
        self.websocket_notifier = WebSocketNotifier()

        self.subject.register_observer(self.websocket_notifier)
        self.subject.register_observer(self.database_saver)

    def process_event(
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
            self.subject.notify_observers(data_success, entity_data)

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

    async def add_websocket_connection(self, websocket):
        await self.websocket_notifier.add_connection(websocket)

    async def remove_websocket_connection(self, websocket):
        await self.websocket_notifier.remove_connection(websocket)

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
