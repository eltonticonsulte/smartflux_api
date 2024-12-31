# -*- coding: utf-8 -*-
from src.repository import (
    CameraRepository,
    UserRepository,
    EmpresaRepository,
    FilialRepository,
    ZoneRepository,
    CountEventRepository,
    CountEventStorageRepository,
)
from src.services import (
    CameraServices,
    UserServices,
    EmpresaServices,
    FilialServices,
    ZoneServices,
    CountEventServices,
    CountEventStorageServices,
)

from src.interfaces import (
    InterfaceCameraService,
    InterfaceUserService,
    InterfaceEmpresaService,
    InterfaceFilialService,
    InterfaceZoneService,
    InterfaceEventCountService,
    InterfaceEventCountStorageService,
)


class FactoryService:
    def __init__(self):
        pass

    def create_camera(self) -> InterfaceCameraService:
        return CameraServices(CameraRepository())

    def create_user(self) -> InterfaceUserService:
        return UserServices(UserRepository())

    def create_empresa(self) -> InterfaceEmpresaService:
        return EmpresaServices(EmpresaRepository())

    def create_filial(self) -> InterfaceFilialService:
        return FilialServices(FilialRepository())

    def create_zone(self) -> InterfaceZoneService:
        return ZoneServices(ZoneRepository())

    def create_count_event(self) -> InterfaceEventCountService:
        return CountEventServices(CountEventRepository())

    def create_count_event_storage(self) -> InterfaceEventCountStorageService:
        return CountEventStorageServices(CountEventStorageRepository())
