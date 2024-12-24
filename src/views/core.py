# -*- coding: utf-8 -*-
from functools import lru_cache
from fastapi.security import OAuth2PasswordBearer
from src.interfaces import (
    InterfaceAuthController,
    InterfaceCameraController,
    InterfaceEmpresaController,
    InterfaceFilialController,
    InterfaceZoneController,
)
from ..compose import FactoryController

auth2_admin = OAuth2PasswordBearer(tokenUrl="api/user/login")
auth2_camera = OAuth2PasswordBearer(tokenUrl="api/camera/login")


controller_auth = FactoryController().create_auth_controller()


def get_controller_auth() -> InterfaceAuthController:
    return controller_auth


@lru_cache()
def get_controller_camera() -> InterfaceCameraController:
    return FactoryController().create_camera_controller()


@lru_cache()
def get_controller_empresa() -> InterfaceEmpresaController:
    return FactoryController().create_empresa_controller()


@lru_cache()
def get_controller_filial() -> InterfaceFilialController:
    return FactoryController().create_filial_controller()


@lru_cache()
def get_controller_zone() -> InterfaceZoneController:
    return FactoryController().create_zone_controller()
