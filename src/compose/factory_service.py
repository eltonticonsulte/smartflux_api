# -*- coding: utf-8 -*-
from src.repository import (
    CameraRepository,
    UserRepository,
    EmpresaRepository,
    FilialRepository,
    ZoneRepository,
    StorageTodayRepository,
    StorageRepository,
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
    StorageTodayServices,
    StorageServices,
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
    InterfaceStorageTodayService,
    InterfaceStorageService,
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
        self.stactic_count_event_websocket = DataEventWebSocketNotifier()

    def get_stactic_count_event_websocket(self) -> InterfaceObserver:
        return self.stactic_count_event_websocket

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
        subject.register_observer(self.get_stactic_count_event_websocket())
        return EventService(CameraRepository(), subject)

    def create_storage(self) -> InterfaceStorageService:
        return StorageServices(StorageRepository())

    def create_storage_today(self) -> InterfaceStorageTodayService:
        return StorageTodayServices(StorageTodayRepository())

    def create_task_update_view(self) -> InterfaceTaskUpdateViewService:
        return TaskUpdateViewService(
            TaskUpdateViewRepository(),
            StorageRepository(),
            StorageTodayRepository(),
        )

    def create_permission(self) -> InterfacePermissionService:
        return PermissionService(PermissionRepository())
