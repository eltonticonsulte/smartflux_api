# -*- coding: utf-8 -*-
import hashlib
from ..database import Usuario
from ..dto import CreateUserRequest, AuthUserResponse, GetUserResponse


class UserMapper:
    @staticmethod
    def auth_entity_to_response(user: Usuario) -> AuthUserResponse:
        return AuthUserResponse(
            username=user.username,
            access_token=user.username,
            token_type="bearer",
            role=user.role,
        )

    @staticmethod
    def create_user_to_entity(user: CreateUserRequest) -> Usuario:
        return Usuario(
            username=user.username,
            password_hash=UserMapper.password_to_hash(user.password),
            role=user.role,
            is_active=True,
        )

    @staticmethod
    def get_entity_to_response(user: Usuario) -> GetUserResponse:
        return GetUserResponse(username=user.username, role=user.role)

    @staticmethod
    def password_to_hash(password: str) -> str:
        salt = "safdasjldkfaoeel"
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hex()
