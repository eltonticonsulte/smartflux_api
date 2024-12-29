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
from ..compose import FactoryController

auth2_admin = OAuth2PasswordBearer(tokenUrl="api/user/login")


@lru_cache()
def get_controller_auth() -> InterfaceAuthService:
    return FactoryController().create_auth_controller()


@lru_cache()
def get_controller_camera() -> InterfaceCameraService:
    return FactoryController().create_camera_controller()


@lru_cache()
def get_controller_empresa() -> InterfaceEmpresaService:
    return FactoryController().create_empresa_controller()


@lru_cache()
def get_controller_filial() -> InterfaceFilialService:
    return FactoryController().create_filial_controller()


@lru_cache()
def get_controller_zone() -> InterfaceZoneService:
    return FactoryController().create_zone_controller()
