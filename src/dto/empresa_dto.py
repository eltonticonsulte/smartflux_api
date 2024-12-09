# -*- coding: utf-8 -*-
from ..common import UserRole


class EmpresaDTO:
    def __init__(
        self,
        username: str,
        password: str,
        is_active: bool = True,
    ):
        self.is_active = is_active
        self.username = username
        self.password = password

    def __repr__(self):
        return f"UserDTO(username={self.username}, password={self.password},is_active={self.is_active})"
