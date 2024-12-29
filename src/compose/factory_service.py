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


class FactoryService:
    def __init__(self):
        pass

    def create_camera(self) -> InterfaceCameraService:
        return CameraServices(CameraRepository())

    def create_auth(self) -> InterfaceAuthService:
        return AuthServices(AuthRepository())

    def create_empresa(self) -> InterfaceEmpresaService:
        return EmpresaServices(EmpresaRepository())

    def create_filial(self) -> InterfaceFilialService:
        return FilialServices(FilialRepository())

    def create_zone(self) -> InterfaceZoneService:
        return ZoneServices(ZoneRepository())
