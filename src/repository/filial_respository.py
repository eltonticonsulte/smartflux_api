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
            result: Filial = self.add(entity)
            return result.filial_id
        except IntegrityError:
            raise RepositoryFilialExecption(f"Filial {filial.name} already exists")
        except Exception as error:
            self.log.critical(error)
            raise error

    def get_all(self) -> List[FilialDTO]:
        with DBConnectionHandler() as session:
            filials = session.query(Filial).all()
            return [FilialMapper.to_dto(filial) for filial in filials]

    def get_by_name(self, name: str) -> FilialDTO:
        with DBConnectionHandler() as session:
            filial = session.query(Filial).filter(Filial.name == name).one_or_none()
            if filial is None:
                raise RepositoryFilialExecption(f"Filial {name} not found")
        return FilialMapper.to_dto(filial)
