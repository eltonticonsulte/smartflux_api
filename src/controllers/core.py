# -*- coding: utf-8 -*-
from functools import lru_cache
from fastapi.security import OAuth2PasswordBearer
from src.interfaces import (
    InterfaceAuthService,
    InterfaceCameraService,
    InterfaceEmpresaService,
    InterfaceFilialService,
    InterfaceZoneService,
)
from ..compose import FactoryService

auth2_admin = OAuth2PasswordBearer(tokenUrl="api/user/login")


@lru_cache()
def get_service_auth() -> InterfaceAuthService:
    return FactoryService().create_auth()


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
