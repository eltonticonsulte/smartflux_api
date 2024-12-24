# -*- coding: utf-8 -*-
import logging
from typing import List
from src.dto.filial_dto import FilialDTO
from src.services.filial_service import FilialServices
from src.interfaces import InterfaceFilialController


class FilialController(InterfaceFilialController):
    def __init__(self, services: FilialServices):
        self.log = logging.getLogger(__name__)
        self.services = services

    def create(self, name: str, cnpj: str, empresa_id: int) -> int:
        return self.services.create(name, cnpj, empresa_id)

    def auth(self, name: str, password: str) -> FilialDTO:
        return self.services.auth(name, password)

    def get_all(self) -> List[FilialDTO]:
        return self.services.get_all()
