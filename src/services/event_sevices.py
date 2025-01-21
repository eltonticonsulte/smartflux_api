# -*- coding: utf-8 -*-
from typing import List
import logging
from src.interfaces import InterfaceEventService
from src.repository import CountEventRepository, CameraRepository
from src.database import EventCountTemp, Camera
from src.dto import (
    EventCountRequest,
    UserPermissionAccessDTO,
    EventCountResponse,
    EventCountDataValidate,
)
from src.mappers import CountEventMapper


class EventService(InterfaceEventService):
    def __init__(
        self,
        camera_repository: CameraRepository,
        event_repository: CountEventRepository,
    ):
        self.log = logging.getLogger(__name__)
        self.camera_repository = camera_repository
        self.event_repository = event_repository

    async def process_event(
        self, events: List[EventCountRequest], user: UserPermissionAccessDTO
    ) -> List[EventCountDataValidate]:
        result_validate: List[EventCountDataValidate] = []
        for event in events:
            result_validate.append(
                CountEventMapper.create_event_request_to_validate(event)
            )

        cameras: List[Camera] = self.camera_repository.get_by_filial(user.filial_id)
        self.check_cameras(result_validate, cameras)
        self.send_database(result_validate)
        return result_validate

    def send_database(self, datas: List[EventCountDataValidate]):
        entitys = [
            CountEventMapper.create_event_validate_to_entity(data) for data in datas
        ]
        self.event_repository.create_all(entitys)

    def check_cameras(self, datas: List[EventCountDataValidate], cameras: List[Camera]):
        for data in datas:
            for camera in cameras:
                if camera.channel_id == data.channel_id:
                    data.camera_name = camera.camera_name
                    data.status = True
                    break
