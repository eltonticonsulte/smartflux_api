# -*- coding: utf-8 -*-
from datetime import datetime
from pydantic import BaseModel


class CreateEmpresaRequest(BaseModel):
    name: str


class CreateEmpresaResponse(BaseModel):
    name: str
    empresa_id: int


class GetEmpresaResponse(BaseModel):
    empresa_id: int
    name: str
    is_active: bool
    data_criacao: datetime
