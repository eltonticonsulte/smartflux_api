# -*- coding: utf-8 -*-
from ..common import UserRole


class EmpresaDTO:
    def __init__(
        self,
        username: str,
        password: str,
        is_active: bool = True,
        filial_id: int = None,
    ):
        self.is_active = is_active
        self.username = username
        self.password = password
        self.filial_id = filial_id

    def __repr__(self):
        return f"EmpresaDTO(username={self.username}, password={self.password},is_active={self.is_active} filial_id={self.filial_id})"
