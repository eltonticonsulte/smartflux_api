# -*- coding: utf-8 -*-
from src.repository import (
    CameraRepository,
    UserRepository,
    EmpresaRepository,
    FilialRepository,
    ZoneRepository,
    TodayEstorageRepository,
    CountEventStorageRepository,
    TaskUpdateViewRepository,
)
from src.services import (
    CameraServices,
    UserServices,
    EmpresaServices,
    FilialServices,
    ZoneServices,
    TodayStorageServices,
    CountEventStorageServices,
    TaskUpdateViewService,
)

from src.interfaces import (
    InterfaceCameraService,
    InterfaceUserService,
    InterfaceEmpresaService,
    InterfaceFilialService,
    InterfaceZoneService,
    InterfaceTodayStorageService,
    InterfaceEventCountStorageService,
    InterfaceTaskUpdateViewService,
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

    def create_count_event(self) -> InterfaceTodayStorageService:
        return TodayStorageServices(TodayEstorageRepository())

    def create_count_event_storage(self) -> InterfaceEventCountStorageService:
        return CountEventStorageServices(CountEventStorageRepository())

    def create_task_update_view(self) -> InterfaceTaskUpdateViewService:
        return TaskUpdateViewService(
            TaskUpdateViewRepository(),
            CountEventStorageRepository(),
            TodayEstorageRepository(),
        )
