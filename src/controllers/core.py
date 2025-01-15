# -*- coding: utf-8 -*-
from functools import lru_cache
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException
from src.enums import UserRule
from src.exceptions import ServiceUserJwtExecption
from src.dto import AuthUserResponse, UserPermissionAccessDTO
from src.interfaces import (
    InterfaceUserService,
    InterfaceCameraService,
    InterfaceEmpresaService,
    InterfaceFilialService,
    InterfaceZoneService,
    InterfaceTodayStorageService,
    InterfaceEventCountStorageService,
    InterfacePermissionService,
    InterfaceEventService,
    InterfaceObserver,
)
from src.compose import FactoryService

auth2_admin = OAuth2PasswordBearer(tokenUrl="api/user/login")
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
def get_service_zone() -> InterfaceZoneService:
    return FactoryService().create_zone()


@lru_cache()
def get_service_count_event() -> InterfaceEventService:
    return factor_service.create_count_event()


@lru_cache()
def get_current_event_websocket() -> InterfaceObserver:
    return factor_service.get_stactic_count_event_websocket()


@lru_cache()
def get_service_count_event_storage() -> InterfaceEventCountStorageService:
    return FactoryService().create_count_event_storage()


@lru_cache()
def get_service_permission() -> InterfacePermissionService:
    return FactoryService().create_permission()


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
                    detail=f"Unauthorized level {user.role} not allowed, min {rule_min}",
                )
        except ServiceUserJwtExecption as error:
            raise HTTPException(401, detail=str(error))
        return user

    return dependency
