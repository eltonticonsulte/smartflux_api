# -*- coding: utf-8 -*-
from pydantic import BaseModel
from ..enums import UserRole


class AuthUserResponse(BaseModel):
    username: str
    user_id: int
    access_token: str
    token_type: str
    role: UserRole


class AuthUserRequest(BaseModel):
    username: str
    password: str


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: UserRole


class GetUserResponse(BaseModel):
    username: str
    role: UserRole

    def is_admin(self):
        return self.role == UserRole.ADMIN

    def is_empresa(self):
        return self.role == UserRole.EMPRESA

    def is_filial(self):
        return self.role == UserRole.FILIAL
