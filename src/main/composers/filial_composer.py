# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import logging
from typing_extensions import Annotated, Doc
from fastapi import Form
from src.repository import FilialRepository
from src.services import FilialServices
from src.controller.filial import FilialController


class FilialComposer:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        repo = FilialRepository()
        self.services = FilialServices(repo)
        self.controller = FilialController(self.services)

    def get_all(self):
        return self.controller.get_all()


class FilialAuthComposer(FilialComposer):
    def __init__(
        self,
        name: Annotated[str, Form(), Doc("name string requeired")],
        token: Annotated[str, Form(), Doc("token string requeired")],
    ):
        super().__init__()
        self.name = name
        self.token = token

    def auth(self):
        return self.controller.auth(self.name, self.token)


class FilialCreateComposer(FilialComposer):
    def __init__(
        self,
        name_filial: Annotated[str, Form(), Doc("name_filial string requeired")],
        cnpj: Annotated[str, Form(), Doc("cnpj string requeired")],
        empresa_id: Annotated[int, Form(), Doc("empresa_id string requeired ")],
    ):
        super().__init__()
        self.name_filial = name_filial
        self.empresa_id = empresa_id
        self.cnpj = cnpj

    def create(self):
        return self.controller.create(self.name_empresa, self.cnpj, self.empresa_id)
