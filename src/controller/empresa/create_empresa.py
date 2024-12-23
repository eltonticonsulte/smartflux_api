# -*- coding: utf-8 -*-
from src.services import EmpresaServices


class EmpresaController:
    def __init__(self, service: EmpresaServices):
        self.service = service

    def create(self, name_empresa: str):
        return self.service.create_empresa(name_empresa)

    def get_all(self):
        return self.service.get_all()
