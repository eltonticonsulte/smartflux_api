# -*- coding: utf-8 -*-
import logging
import uuid
from typing import List
from src.dto import CountEventDTO
from src.services import CameraServices
from src.interfaces import InterfaceCameraController


class CameraController(InterfaceCameraController):
    def __init__(self, services: CameraServices):
        self.log = logging.getLogger(__name__)
        self.services = services

    def create(self, name: str, zone_id: int):
        return self.services.create(name, zone_id)

    def get_all(self):
        return self.services.get_all()

    def get_by_name(self, name: str):
        return self.services.get_by_name(name)

    def validate_token(self, token: uuid.UUID):
        return self.services.validate_token(token)

    def register_event(self, data: List[CountEventDTO]) -> dict:
        return self.services.register_event(data)
