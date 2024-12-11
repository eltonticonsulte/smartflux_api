# -*- coding: utf-8 -*-
from ..database import Filial
from ..dto import FilialDTO


class FilialMapper:
    @staticmethod
    def to_dto(empresa: Filial) -> FilialDTO:
        return FilialDTO(
            name=empresa.name,
            cnpj=empresa.cnpj,
            password_hash=empresa.password_hash,
            token_api=empresa.token_api,
            description=empresa.description,
            is_active=empresa.is_active,
            empresa_id=empresa.empresa_id,
        )

    @staticmethod
    def to_entity(empresa: FilialDTO) -> Filial:
        return Filial(
            name=empresa.name,
            cnpj=empresa.cnpj,
            password_hash=empresa.password_hash,
            token_api=empresa.token_api,
            description=empresa.description,
            is_active=empresa.is_active,
            empresa_id=empresa.empresa_id,
        )
