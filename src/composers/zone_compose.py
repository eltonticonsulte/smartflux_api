# -*- coding: utf-8 -*-
from logging import getLogger
from typing_extensions import Annotated, Doc
from fastapi import Form
from src.repository.zone_repository import ZoneRepository
from src.services.zone_service import ZoneServices
from src.controller.zone_controller import ZoneController


class BaseZoneCompose:
    def __init__(self):
        self.log = getLogger(__name__)
        repo = ZoneRepository()
        service = ZoneServices(repo)
        self.controller = ZoneController(service)


class CreateZoneCompose(BaseZoneCompose):
    def __init__(
        self,
        *,
        name: Annotated[str, Form(), Doc("name string requeired")],
        id_filial: Annotated[int, Form(), Doc("id_filial string requeired")],
    ):
        super().__init__()
        self.name = name
        self.id_filial = id_filial


class GetZoneCompose(BaseZoneCompose):
    def __init__(self):
        super().__init__()

    def get_all(self):
        return self.controller.get_all()
