# -*- coding: utf-8 -*-
import logging
from typing import List
from .base_repository import BaseRepository
from ..database import Filial, DBConnectionHandler, IntegrityError
from ..dto import FilialDTO
from ..mappers import FilialMapper


class RepositoryFilialExecption(Exception):
    def __init__(self, message):
        super().__init__(message)


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
        except IntegrityError:
            raise RepositoryFilialExecption(f"Filial {filial.name} already exists")
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
                raise RepositoryFilialExecption(f"Filial {name} not found")
        return FilialMapper.to_dto(filial)
