# -*- coding: utf-8 -*-
from typing import List
from ..database import DBConnectionHandler, PermissaoAcesso


class PermissaoRepository:
    def __init__(self):
        pass

    def fetch_permisso_by_user(self, user_id: int) -> List[PermissaoAcesso]:
        with DBConnectionHandler() as session:
            return session.query(PermissaoAcesso).filter_by(user_id=user_id).all()
