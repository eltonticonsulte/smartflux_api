# -*- coding: utf-8 -*-

from pydantic import BaseModel


class RequestCreatePermission(BaseModel):
    user_id: int
    empresa_id: int
    filial_id: int


class ResponsePermission(BaseModel):
    permissao_id: int
    user_id: int
    empresa_id: int
    filial_id: int
