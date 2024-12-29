# -*- coding: utf-8 -*-
from ..database import Filial
from ..dto import CreateFilialRequest, CreateFilialResponse, GetFilialResponse


class FilialMapper:
    @staticmethod
    def create_request_to_entity(new_filial: CreateFilialRequest) -> Filial:
        return Filial(
            name=new_filial.name_filial,
            cnpj=new_filial.cnpj,
            empresa_id=new_filial.empresa_id,
        )

    @staticmethod
    def create_entity_to_response(filial: Filial) -> CreateFilialResponse:
        return CreateFilialResponse(filial_id=filial.filial_id, name_filial=filial.name)

    @staticmethod
    def get_entity_to_response(filial: Filial) -> GetFilialResponse:
        return GetFilialResponse(
            filial_id=filial.filial_id,
            name=filial.name,
            cnpj=filial.cnpj,
            is_active=filial.is_active,
            empresa_id=filial.empresa_id,
        )
