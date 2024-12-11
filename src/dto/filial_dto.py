# -*- coding: utf-8 -*-
from ..common import UserRole


class FilialDTO:
    def __init__(
        self,
        name: str,
        cnpj: str,
        password_hash: str = "",
        token_api: str = "",
        is_active: bool = True,
        description: str = "",
        empresa_id: int = None,
    ):
        self.is_active = is_active
        self.name = name
        self.cnpj = cnpj
        self.password_hash = password_hash
        self.token_api = token_api
        self.description = description
        self.empresa_id = empresa_id

    def to_dict(self):
        return {
            "name": self.name,
            "cnpj": self.cnpj,
            "password_hash": self.password_hash,
            "token_api": self.token_api,
            "is_active": self.is_active,
            "description": self.description,
            "empresa_id": self.empresa_id,
        }

    def __repr__(self):
        return f"FilialDTO(name={self.name}, cnpj={self.cnpj}, password_hash={self.password_hash}, token_api={self.token_api}, is_active={self.is_active}, description={self.description}, empresa_id={self.empresa_id})"
