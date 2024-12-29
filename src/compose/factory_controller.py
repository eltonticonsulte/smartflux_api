# -*- coding: utf-8 -*-
from src.repository import (
    CameraRepository,
    AuthRepository,
    EmpresaRepository,
    FilialRepository,
    ZoneRepository,
)
from src.services import (
    CameraServices,
    AuthServices,
    EmpresaServices,
    FilialServices,
    ZoneServices,
)

from src.interfaces import (
    InterfaceCameraService,
    InterfaceAuthService,
    InterfaceEmpresaService,
    InterfaceFilialService,
    InterfaceZoneService,
)


class FactoryController:
    def __init__(self):
        pass

    def create_camera_controller(self) -> InterfaceCameraService:
        return CameraServices(CameraRepository())

    def create_auth_controller(self) -> InterfaceAuthService:
        return AuthServices(AuthRepository())

    def create_empresa_controller(self) -> InterfaceEmpresaService:
        return EmpresaServices(EmpresaRepository())

    def create_filial_controller(self) -> InterfaceFilialService:
        return FilialServices(FilialRepository())

    def create_zone_controller(self) -> InterfaceZoneService:
        return ZoneServices(ZoneRepository())
