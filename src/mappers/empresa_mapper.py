# -*- coding: utf-8 -*-
from ..database import Empresa
from ..dto import EmpresaDTO


class EmpresaMapper:
    @staticmethod
    def to_dto(empresa: Empresa) -> EmpresaDTO:
        return EmpresaDTO(
            name=empresa.name, empresa_id=empresa.id, is_active=empresa.is_active
        )

    @staticmethod
    def to_entity(empresa: EmpresaDTO) -> Empresa:

        return Empresa(
            name=empresa.name, id=empresa.empresa_id, is_active=empresa.is_active
        )
