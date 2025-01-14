# -*- coding: utf-8 -*-
from functools import lru_cache
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException
from src.enums import UserRule
from src.dto import AuthUserResponse, UserPermissionAccessDTO
from src.interfaces import (
    InterfaceUserService,
    InterfaceCameraService,
    InterfaceEmpresaService,
    InterfaceFilialService,
    InterfaceZoneService,
    InterfaceTodayStorageService,
    InterfaceEventCountStorageService,
)
from src.compose import FactoryService

auth2_admin = OAuth2PasswordBearer(tokenUrl="api/user/login")


@lru_cache()
def get_service_user() -> InterfaceUserService:
    return FactoryService().create_user()


@lru_cache()
def get_service_camera() -> InterfaceCameraService:
    return FactoryService().create_camera()


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
def get_service_count_event() -> InterfaceTodayStorageService:
    return FactoryService().create_count_event()


@lru_cache()
def get_service_count_event_storage() -> InterfaceEventCountStorageService:
    return FactoryService().create_count_event_storage()


def rule_require(rule_min: UserRule):
    def dependency(
        token: str = Depends(auth2_admin),
        user_service: InterfaceUserService = Depends(get_service_user),
    ) -> UserPermissionAccessDTO:
        user: UserPermissionAccessDTO = user_service.current_user(token)
        if user.rule.value > rule_min.value:
            raise HTTPException(
                401,
                detail=f"Unauthorized level {user.role} not allowed, min {rule_min}",
            )
        return user

    return dependency
