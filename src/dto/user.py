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

    def is_admin(self):
        return self.role == UserRule.ADMIN

    def is_empresa(self):
        return self.role == UserRule.EMPRESA

    def is_filial(self):
        return self.role == UserRule.FILIAL
