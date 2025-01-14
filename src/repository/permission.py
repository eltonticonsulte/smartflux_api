# -*- coding: utf-8 -*-
import logging
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from src.database import Usuario, DBConnectionHandler, PermissaoAcesso, Empresa, Filial
from src.dto import CreatePermissionRequest


class PermissionRepository:
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, entity: PermissaoAcesso) -> int:
        with DBConnectionHandler() as session:
            session.add(entity)
            session.commit()
            return entity.permissao_id

    def fetch_user_not_permission(self) -> List[PermissaoAcesso]:
        with DBConnectionHandler() as session:
            return (
                session.query(Usuario)
                .join(PermissaoAcesso, PermissaoAcesso.user_id == Usuario.user_id)
                .filter(
                    PermissaoAcesso.user_id == None
                )  # Filtra usuários sem permissões
                .all()
            )

    def fetch_permisso_by_user(self, user_id: int) -> PermissaoAcesso:
        with DBConnectionHandler() as session:
            return (
                session.query(PermissaoAcesso)
                .filter(PermissaoAcesso.user_id == user_id)
                .first()
            )
