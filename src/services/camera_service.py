# -*- coding: utf-8 -*-
import logging
from typing import List
from ..repository import CameraRepository
from ..dto import CameraDTO


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
