# -*- coding: utf-8 -*-
from pydantic import BaseModel


class CreateFilialRequest(BaseModel):
    name_filial: str
    empresa_id: int
    cnpj: str


class CreateFilialResponse(BaseModel):
    filial_id: int
    name_filial: str


class GetFilialResponse(BaseModel):
    filial_id: int
    name: str
    cnpj: str
    is_active: bool
    empresa_id: int
