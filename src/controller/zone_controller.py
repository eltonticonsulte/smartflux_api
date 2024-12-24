# -*- coding: utf-8 -*-
from src.services.zone_service import ZoneServices
from src.interfaces import InterfaceZoneController
import logging


class ZoneController(InterfaceZoneController):
    def __init__(self, services: ZoneServices):
        self.log = logging.getLogger(__name__)
        self.services = services

    def create(self, name: str):
        return self.services.create(name)

    def get_all(self):
        return self.services.get_all()
