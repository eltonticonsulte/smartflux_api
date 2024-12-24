# -*- coding: utf-8 -*-
from src.repository import (
    CameraRepository,
    AuthRepository,
    EmpresaRepository,
    FilialRepository,
    ZoneRepository,
    CounterEventRepository,
)
from src.services import (
    CameraServices,
    AuthServices,
    EmpresaServices,
    FilialServices,
    ZoneServices,
    CountEventServices,
)
from src.controller import (
    CameraController,
    AuthController,
    EmpresaController,
    FilialController,
    ZoneController,
    CounterEventController,
)
from src.interfaces import (
    InterfaceCameraController,
    InterfaceAuthController,
    InterfaceEmpresaController,
    InterfaceFilialController,
    InterfaceZoneController,
)


class FactoryController:
    def __init__(self):
        pass

    def create_camera_controller(self) -> InterfaceCameraController:
        return CameraController(CameraServices(CameraRepository()))

    def create_auth_controller(self) -> InterfaceAuthController:
        return AuthController(AuthServices(AuthRepository()))

    def create_empresa_controller(self) -> InterfaceEmpresaController:
        return EmpresaController(EmpresaServices(EmpresaRepository()))

    def create_filial_controller(self) -> InterfaceFilialController:
        return FilialController(FilialServices(FilialRepository()))

    def create_zone_controller(self) -> InterfaceZoneController:
        return ZoneController(ZoneServices(ZoneRepository()))

    def create_counter_event_controller(self) -> CounterEventController:
        return CounterEventController(CountEventServices(CounterEventRepository()))
