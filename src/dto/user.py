# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel
from src.enums import UserRule


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
    permission_id: Optional[int] = None
    empresa_id: Optional[int] = None
    filial_id: Optional[int] = None
    user_id: int
    rule: UserRule
    username: str
    is_active: bool
