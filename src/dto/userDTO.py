# -*- coding: utf-8 -*-
from ..common import UserRole


class UserDTO:
    def __init__(
        self,
        username: str,
        password: str,
        role: UserRole = UserRole.FILIAL,
        is_active: bool = True,
    ):
        self.is_active = is_active
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f"UserDTO(username={self.username}, password={self.password}, role={self.role})"
