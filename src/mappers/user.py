# -*- coding: utf-8 -*-
import hashlib
from src.database import Usuario, PermissaoAcesso
from src.dto import (
    CreateUserRequest,
    AuthUserResponse,
    GetUserResponse,
    UserPermissionAccessDTO,
)


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
        return GetUserResponse(
            user_id=user.user_id, username=user.username, role=user.role
        )

    @staticmethod
    def password_to_hash(password: str) -> str:
        salt = "safdasjldkfaoeel"
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hex()

    @staticmethod
    def to_permissao(
        user: Usuario, permissao: PermissaoAcesso
    ) -> UserPermissionAccessDTO:
        if permissao is None:
            return UserPermissionAccessDTO(
                permission_id=None,
                user_id=user.user_id,
                empresa_id=None,
                filial_id=None,
                rule=user.role,
                username=user.username,
                is_active=user.is_active,
            )

        return UserPermissionAccessDTO(
            permission_id=permissao.permissao_id,
            user_id=permissao.user_id,
            empresa_id=permissao.empresa_id,
            filial_id=permissao.filial_id,
            rule=user.role,
            username=user.username,
            is_active=user.is_active,
        )
