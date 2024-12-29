# -*- coding: utf-8 -*-
from pydantic import BaseModel
from ..common import UserRole


class AuthUserResponse(BaseModel):
    username: str
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


class CreateUserResponse(BaseModel):
    username: str
