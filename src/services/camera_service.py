# -*- coding: utf-8 -*-
import logging
import uuid
from typing import List
from ..repository import CameraRepository
from ..dto import CameraDTO, CountEventDTO
from ..mappers import CountEventMapper


class CameraServices:
    def __init__(self, repository: CameraRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, camera: CameraDTO) -> bool:
        cam: CameraDTO = self.repository.get_by_name(camera.name)
        if cam.name != "":
            raise ValueError("camera name already exists")

        return self.repository.create_user(camera)

    def get_by_name(self, name: str) -> CameraDTO:
        return self.repository.get_by_name(name)

    def get_all(self) -> List[CameraDTO]:
        return self.repository.get_all()

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
