# -*- coding: utf-8 -*-
import hashlib
from ..database import UserRole, Usuario
from ..dto import userDTO


class UserMapper:
    @staticmethod
    def to_dto(user: Usuario) -> userDTO:
        return userDTO(
            username=user.username,
            password=user.password_hash,
            role=user.role,
            is_active=user.is_active,
        )

    @staticmethod
    def to_entity(user: userDTO) -> Usuario:
        salt = "safdasjldkfaoeel"
        hash_password = hashlib.pbkdf2_hmac(
            "sha256", user.password.encode("utf-8"), salt.encode("utf-8"), 100000
        ).hexdigest()
        return Usuario(
            username=user.username,
            password_hash=hash_password,
            role=user.role,
            is_active=user.is_active,
        )
