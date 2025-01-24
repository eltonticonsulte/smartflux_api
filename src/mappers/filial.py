# -*- coding: utf-8 -*-
from ..database import Filial
from ..dto import (
    RequestCreateFilial,
    ResponseFilial,
    RequestUpdateFilial,
)


class FilialMapper:
    @staticmethod
    def create_request_to_entity(new_filial: RequestCreateFilial) -> Filial:
        return Filial(
            name=new_filial.name_filial,
            cnpj=new_filial.cnpj,
            empresa_id=new_filial.empresa_id,
        )

    @staticmethod
    def get_entity_to_response(filial: Filial) -> ResponseFilial:
        return ResponseFilial(
            filial_id=filial.filial_id,
            token=filial.token_api,
            name=filial.name,
            cnpj=filial.cnpj,
            is_active=filial.is_active,
            empresa_id=filial.empresa_id,
        )

    @staticmethod
    def update_request_to_entity(filial_id: int, filial: RequestUpdateFilial) -> Filial:
        up_filial = Filial(filial_id=filial_id)

        if filial.name is not None:
            up_filial.name = filial.name

        if filial.cnpj is not None:
            up_filial.cnpj = filial.cnpj

        if filial.is_active is not None:
            up_filial.is_active = filial.is_active

        return up_filial
