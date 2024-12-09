# -*- coding: utf-8 -*-
import hashlib
from ..database import UserRole, Usuario
from ..dto import UserDTO


class UserMapper:
    @staticmethod
    def to_dto(user: Usuario) -> UserDTO:
        return UserDTO(
            username=user.username,
            password="",
            hash_password=user.password_hash,
            role=user.role,
            is_active=user.is_active,
        )

    @staticmethod
    def to_entity(user: UserDTO) -> Usuario:
        salt = "safdasjldkfaoeel"
        hash_password = hashlib.pbkdf2_hmac(
            "sha256", user.password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hex()
        return Usuario(
            username=user.username,
            password_hash=hash_password,
            role=user.role,
            is_active=user.is_active,
        )
