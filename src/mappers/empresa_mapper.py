# -*- coding: utf-8 -*-
from ..database import Empresa
from ..dto import EmpresaDTO


class EmpresaMapper:
    @staticmethod
    def to_dto(empresa: Empresa) -> EmpresaDTO:
        return EmpresaDTO(name=empresa.name, is_active=empresa.is_active)

    @staticmethod
    def to_entity(empresa: EmpresaDTO) -> Empresa:

        return Empresa(name=empresa.name, is_active=empresa.is_active)
