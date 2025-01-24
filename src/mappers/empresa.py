# -*- coding: utf-8 -*-
from ..database import Empresa
from ..dto import (
    RequestCreateEmpresa,
    ResponseEmpresa,
    ResquestUpdateEmpresa,
)


class EmpresaMapper:
    @staticmethod
    def get_entity_to_response(empresa: Empresa) -> ResponseEmpresa:
        return ResponseEmpresa(
            empresa_id=empresa.empresa_id,
            name=empresa.name,
            is_active=empresa.is_active,
            description=empresa.description,
            data_criacao=empresa.data_criacao,
        )

    @staticmethod
    def create_request_to_entity(new_empresa: RequestCreateEmpresa) -> Empresa:
        return Empresa(name=new_empresa.name)

    @staticmethod
    def update_request_to_entity(
        empresa_id: int, empresa: ResquestUpdateEmpresa
    ) -> Empresa:
        up_empreas = Empresa(empresa_id=empresa_id)

        if empresa.name is not None:
            up_empreas.name = empresa.name

        if empresa.is_active is not None:
            up_empreas.is_active = empresa.is_active

        if empresa.description is not None:
            up_empreas.description = empresa.description

        return up_empreas
