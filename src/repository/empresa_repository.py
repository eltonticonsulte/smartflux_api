# -*- coding: utf-8 -*-
import logging
from typing import List
from .base_repository import BaseRepository
from ..database import Empresa
from ..database import IntegrityError, DBConnectionHandler
from ..dto import EmpresaDTO
from ..mappers import EmpresaMapper


class RepositoryEmpresaExecption(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class EmpresaRepository(BaseRepository):
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def create(self, name: str) -> int:
        self.log.debug(f"create_empresa {name}")
        db_empresa = Empresa(name=name, is_active=True)
        try:
            return self.add(db_empresa)
        except IntegrityError:
            raise RepositoryEmpresaExecption(f"Empresa {name} already exists")
        except Exception as error:
            self.log.critical(error)
            raise error

    def get_all(self) -> List[EmpresaDTO]:
        empresas = super().get_all(Empresa)
        return [EmpresaMapper.to_dto(empresa) for empresa in empresas]

    def get_empresa_by_name(self, name: str) -> Empresa:
        empresa = super().get_by_name(Empresa, name)
        if empresa is None:
            raise RepositoryEmpresaExecption(f"Empresa {name} not found")
        return EmpresaMapper.to_dto(empresa)
