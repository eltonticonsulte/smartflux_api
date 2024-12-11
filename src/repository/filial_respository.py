# -*- coding: utf-8 -*-
import logging
from typing import List
from .base_repository import BaseRepository
from ..database import Filial, DBConnectionHandler
from ..dto import FilialDTO
from ..mappers import FilialMapper


class FilialRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, filial: FilialDTO) -> int:
        entity = Filial(
            name=filial.name,
            cnpj=filial.cnpj,
            empresa_id=filial.empresa_id,
        )
        try:
            return self.add(entity)
        except Exception as error:
            self.log.critical(error)
            raise error

    def get_all(self) -> List[FilialDTO]:
        result = super().get_all(Filial)
        return [FilialMapper.to_dto(filial) for filial in result]

    def get_by_name(self, name: str) -> FilialDTO:
        with DBConnectionHandler() as session:
            filial = session.query(Filial).filter(Filial.name == name).one_or_none()
            if filial is None:
                return FilialDTO(name=name, cnpj="")
        return FilialMapper.to_dto(filial)
