# -*- coding: utf-8 -*-
from pydantic import BaseModel
from ..enums import UserRule


class AuthUserResponse(BaseModel):
    username: str
    user_id: int
    access_token: str
    token_type: str
    role: UserRule


class AuthUserRequest(BaseModel):
    username: str
    password: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: UserRule


class GetUserResponse(BaseModel):
    username: str
    role: UserRule


class UserPermissionAccessDTO(BaseModel):
    permission_id: int
    empresa_id: int
    filial_id: int
    user_id: int
    rule: UserRule
    username: str
    is_active: bool
