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
    PermissionRepository,
    CountEventRepository,
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
    PermissionService,
    EventService,
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
    InterfacePermissionService,
    InterfaceEventService,
    InterfaceObserver,
)
from src.observers import (
    SubjectEventCount,
    DataEventCountSave,
    DataEventWebSocketNotifier,
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

    def create_count_event(self) -> InterfaceEventService:
        subject = SubjectEventCount()
        subject.register_observer(DataEventCountSave(CountEventRepository()))
        subject.register_observer(DataEventWebSocketNotifier())
        return EventService(CameraRepository(), subject)

    def create_count_event_storage(self) -> InterfaceEventCountStorageService:
        return CountEventStorageServices(CountEventStorageRepository())

    def create_task_update_view(self) -> InterfaceTaskUpdateViewService:
        return TaskUpdateViewService(
            TaskUpdateViewRepository(),
            CountEventStorageRepository(),
            TodayEstorageRepository(),
        )

    def create_permission(self) -> InterfacePermissionService:
        return PermissionService(PermissionRepository())
