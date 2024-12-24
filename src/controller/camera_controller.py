# -*- coding: utf-8 -*-
from src.services import CameraServices
import logging
from src.interfaces import InterfaceCameraController


class CameraController(InterfaceCameraController):
    def __init__(self, services: CameraServices):
        self.log = logging.getLogger(__name__)
        self.services = services

    def create(self, name: str):
        return self.services.create(name)

    def get_all(self):
        return self.services.get_all()

    def get_by_name(self, name: str):
        return self.services.get_by_name(name)
