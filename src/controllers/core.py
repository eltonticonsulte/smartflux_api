# -*- coding: utf-8 -*-
from functools import lru_cache
from fastapi.security.api_key import APIKeyHeader
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Security
from core import get_settings
from src.enums import UserRule
from src.exceptions import ServiceUserJwtExecption
from src.dto import UserPermissionAccessDTO, ResponseFilial
from src.interfaces import (
    InterfaceUserService,
    InterfaceCameraService,
    InterfaceEmpresaService,
    InterfaceFilialService,
    InterfaceStorageService,
    InterfacePermissionService,
    InterfaceEventService,
)
from src.compose import FactoryService

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)
auth2_admin = OAuth2PasswordBearer(tokenUrl=f"{get_settings().API_V1_STR}/user/login")
factor_service = FactoryService()


@lru_cache()
def get_service_user() -> InterfaceUserService:
    return factor_service.create_user()


@lru_cache()
def get_service_camera() -> InterfaceCameraService:
    return factor_service.create_camera()


@lru_cache()
def get_service_empresa() -> InterfaceEmpresaService:
    return FactoryService().create_empresa()


@lru_cache()
def get_service_filial() -> InterfaceFilialService:
    return FactoryService().create_filial()


@lru_cache()
def get_service_count_event() -> InterfaceEventService:
    return factor_service.create_count_event()


@lru_cache()
def get_service_storage() -> InterfaceStorageService:
    return FactoryService().create_storage()


@lru_cache()
def get_service_permission() -> InterfacePermissionService:
    return FactoryService().create_permission()


def verificar_api_key(
    api_key: str = Security(api_key_header),
    service_filial: InterfaceFilialService = Depends(get_service_filial),
):
    try:
        result: ResponseFilial = service_filial.get_by_token(api_key)
    except Exception as error:
        raise HTTPException(status_code=403, detail=str(error))
    return result


def rule_require(rule_min: UserRule):
    def dependency(
        token: str = Depends(auth2_admin),
        user_service: InterfaceUserService = Depends(get_service_user),
    ) -> UserPermissionAccessDTO:
        try:
            user: UserPermissionAccessDTO = user_service.current_user(token)
            if not user.is_active:
                raise HTTPException(401, detail="Usuário inativo")
            if user.rule.value > rule_min.value:
                raise HTTPException(
                    401,
                    detail=f"Unauthorized level {user.rule} not allowed, min {rule_min}",
                )
        except ServiceUserJwtExecption as error:
            raise HTTPException(401, detail=str(error))
        return user

    return dependency
