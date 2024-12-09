# -*- coding: utf-8 -*-
from ..common import UserRole


class UserDTO:
    def __init__(
        self,
        username: str,
        password: str,
        hash_password: str = "",
        role: UserRole = UserRole.FILIAL,
        is_active: bool = True,
    ):
        self.is_active = is_active
        self.username = username
        self.password = password
        self.hash_password = hash_password
        self.role = role

    def __repr__(self):
        return f"UserDTO(username={self.username}, password={self.password}, hash_password={self.hash_password}, role={self.role}, is_active={self.is_active})"
