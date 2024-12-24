# -*- coding: utf-8 -*-
import logging
from typing_extensions import Annotated, Doc
from fastapi import Form
from src.repository import EmpresaRepository
from src.services import EmpresaServices
from src.controller.empresa import EmpresaController


class EmpresaComposer:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        repo = EmpresaRepository()
        self.empresa_services = EmpresaServices(repo)
        self.controller = EmpresaController(self.empresa_services)

    def get_all(self):
        return self.controller.get_all()


class CreateEmpresaComposer(EmpresaComposer):
    def __init__(
        self,
        name_empresa: Annotated[
            str, Form(), Doc("name_empresa string requeired for authentication")
        ],
    ):
        super().__init__()
        self.name_empresa = name_empresa

    def create(self):
        return self.controller.create(self.name_empresa)
