# -*- coding: utf-8 -*-
import logging
import uuid
from typing import List
from ..repository import CameraRepository
from ..dto import (
    CountEventDTO,
    CreateCameraRequest,
    CreateCameraResponse,
    GetCameraResponse,
)
from ..mappers import CountEventMapper, CameraMapper


class CameraServices:
    def __init__(self, repository: CameraRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, request: CreateCameraRequest) -> CreateCameraResponse:
        new_camera = CameraMapper.create_request_to_entity(request)
        camera_id = self.repository.create(new_camera)
        return CreateCameraResponse(camera_id=camera_id, name=new_camera.name)

    # def get_by_name(self, name: str) -> CameraDTO:
    #    return self.repository.get_by_name(name)

    def get_all(self) -> List[GetCameraResponse]:
        datas = self.repository.get_all()
        result = [CameraMapper.get_entity_to_response(camera) for camera in datas]
        return result

    def validate_token(self, token: uuid.UUID):
        self.log.debug(f"validate_token {token}")
        self.repository.validade_token(token)

    def register_event(self, data: List[CountEventDTO]):
        self.log.debug(f"register_event {data}")
        data_success, data_fail = self.check_chennel(data)
        if data_success:
            [CountEventMapper.to_entity(data) for data in data_success]
            self.repository.add_all(data_success)
        resutl = {"id_sucess": [], "id_fail": []}
        for data in data_success:
            resutl["id_sucess"].append(data.event_id)
        for data in data_fail:
            resutl["id_fail"].append(data.event_id)
        return resutl

    def check_chennel(self, datas: List[CountEventDTO]) -> bool:
        cameras = self.repository.get_all()
        datas_fail = []
        data_success = []
        tokens = [camera.channel_id for camera in cameras]
        for data in datas:
            if data.channel_id not in tokens:
                datas_fail.append(data)
            else:
                data_success.append(data)
        return data_success, datas_fail
