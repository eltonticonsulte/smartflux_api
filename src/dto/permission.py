# -*- coding: utf-8 -*-

from pydantic import BaseModel


class CreatePermissionRequest(BaseModel):
    user_id: int
    empresa_id: int
    filial_id: int


class PermissionResponse(BaseModel):
    permissao_id: int
    user_id: int
    empresa_id: int
    filial_id: int


class DataPermission(BaseModel):
    user_id: int
    empresa_id: int
    filial_id: int
