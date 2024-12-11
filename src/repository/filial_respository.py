# -*- coding: utf-8 -*-
import logging
from .base_repository import BaseRepository
from ..database import Filial, DBConnectionHandler
from ..dto import FilialDTO


class FilialRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, filial: FilialDTO) -> int:
        entity = Filial(
            name=filial.name,
            cnpj=filial.cnpj,
            empresa_id=filial.empresa_id,
            password_hash=filial.password_hash,
        )
        try:
            return self.add(entity)
        except Exception as error:
            self.log.critical(error)
            raise error
