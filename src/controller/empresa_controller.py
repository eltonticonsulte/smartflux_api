# -*- coding: utf-8 -*-
from typing import List
from src.services import EmpresaServices
from src.dto import EmpresaDTO
from src.interfaces import InterfaceEmpresaController


class EmpresaController(InterfaceEmpresaController):
    def __init__(self, service: EmpresaServices):
        self.service = service

    def create(self, name_empresa: str):
        return self.service.create_empresa(name_empresa)

    def get_all(self) -> List[EmpresaDTO]:
        return self.service.get_all()
