# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RequestCreateEmpresa(BaseModel):
    name: str


class ResponseEmpresa(BaseModel):
    empresa_id: int
    name: str
    is_active: bool
    data_criacao: datetime
    description: str


class ResquestUpdateEmpresa(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None
