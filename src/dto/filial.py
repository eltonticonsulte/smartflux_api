# -*- coding: utf-8 -*-
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class RequestCreateFilial(BaseModel):
    name_filial: str
    empresa_id: int
    cnpj: str


class ResponseFilial(BaseModel):
    filial_id: int
    token: UUID
    name: str
    cnpj: str
    is_active: bool
    empresa_id: int


class RequestUpdateFilial(BaseModel):
    name: Optional[str] = None
    cnpj: Optional[str] = None
    is_active: Optional[bool] = None
