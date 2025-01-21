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
    WebSocketNotifierService,
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
)
from src.observers import (
    SubjectEventCount,
    DataEventCountSave,
)
from src.external import DataEventWebSocketNotifier


class FactoryService:
    def __init__(self):
        pass

    def create_websocket(self) -> WebSocketNotifierService:
        return WebSocketNotifierService(
            WebSocketNotifierService(), self.create_user(), DataEventWebSocketNotifier()
        )

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
        return EventService(CameraRepository(), CountEventRepository())

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
