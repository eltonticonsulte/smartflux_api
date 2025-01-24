# -*- coding: utf-8 -*-
from src.dto import ResponsePermission, RequestCreatePermission
from src.database import PermissaoAcesso


class MapperPermission:
    @staticmethod
    def create_to_entity(permission: RequestCreatePermission) -> PermissaoAcesso:
        return PermissaoAcesso(
            user_id=permission.user_id,
            empresa_id=permission.empresa_id,
            filial_id=permission.filial_id,
        )
