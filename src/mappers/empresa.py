# -*- coding: utf-8 -*-
from ..database import Empresa
from ..dto import (
    CreateRequestEmpresa,
    CreateResponseEmpresa,
    GetResponseEmpresa,
)


class EmpresaMapper:
    @staticmethod
    def get_entity_to_response(empresa: Empresa) -> GetResponseEmpresa:
        return GetResponseEmpresa(
            empresa_id=empresa.empresa_id,
            name=empresa.name,
            is_active=empresa.is_active,
            data_criacao=empresa.data_criacao,
        )

    @staticmethod
    def create_entity_to_response(empresa: Empresa) -> CreateResponseEmpresa:
        return CreateResponseEmpresa(empresa_id=empresa.empresa_id)

    @staticmethod
    def create_request_to_entity(new_empresa: CreateRequestEmpresa) -> Empresa:
        return Empresa(name=new_empresa.name)
