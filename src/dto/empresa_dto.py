# -*- coding: utf-8 -*-
from ..common import UserRole


class EmpresaDTO:
    def __init__(
        self,
        name: str,
        is_active: bool = True,
    ):
        self.is_active = is_active
        self.name = name

    def to_dict(self):
        return {
            "name": self.name,
            "is_active": self.is_active,
        }

    def __repr__(self):
        return f"EmpresaDTO(name={self.name},is_active={self.is_active})"
