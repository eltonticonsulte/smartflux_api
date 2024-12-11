# -*- coding: utf-8 -*-
from ..common import UserRole


class EmpresaDTO:
    def __init__(self, name: str, is_active: bool = True, empresa_id: int = None):
        self.is_active = is_active
        self.name = name
        self.empresa_id = empresa_id

    def to_dict(self):
        return {"name": self.name, "is_active": self.is_active, "id": self.empresa_id}

    def __repr__(self):
        return f"EmpresaDTO(name={self.name},is_active={self.is_active}, id={self.empresa_id})"
