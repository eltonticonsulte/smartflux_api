# -*- coding: utf-8 -*-
from datetime import datetime
from pydantic import BaseModel


class CreateRequestEmpresa(BaseModel):
    name: str


class CreateResponseEmpresa(BaseModel):
    name: str
    empresa_id: int


class GetResponseEmpresa(BaseModel):
    empresa_id: int
    name: str
    is_active: bool
    data_criacao: datetime
