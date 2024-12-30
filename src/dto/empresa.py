# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
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
    description: str


class UpdateEmpresaRequest(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None
