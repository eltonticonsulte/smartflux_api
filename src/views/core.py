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


@lru_cache()
def controller_auth(self) -> InterfaceAuthController:
    return FactoryController().create_auth_controller()


@lru_cache()
def controller_camera(self) -> InterfaceCameraController:
    return FactoryController().create_camera_controller()


@lru_cache()
def controller_empresa(self) -> InterfaceEmpresaController:
    return FactoryController().create_empresa_controller()


@lru_cache()
def controller_filial(self) -> InterfaceFilialController:
    return FactoryController().create_filial_controller()


@lru_cache()
def controller_zone(self) -> InterfaceZoneController:
    return FactoryController().create_zone_controller()
