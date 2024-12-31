# -*- coding: utf-8 -*-
from functools import lru_cache
from fastapi.security import OAuth2PasswordBearer
from src.interfaces import (
    InterfaceUserService,
    InterfaceCameraService,
    InterfaceEmpresaService,
    InterfaceFilialService,
    InterfaceZoneService,
    InterfaceEventCountService,
    InterfaceEventCountStorageService,
)
from ..compose import FactoryService

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
def get_service_count_event() -> InterfaceEventCountService:
    return FactoryService().create_count_event()


@lru_cache()
def get_service_count_event_storage() -> InterfaceEventCountStorageService:
    return FactoryService().create_count_event_storage()
