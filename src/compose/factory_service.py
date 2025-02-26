# -*- coding: utf-8 -*-
from src.repository import (
    CameraRepository,
    UserRepository,
    EmpresaRepository,
    FilialRepository,
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
    InterfaceStorageTodayService,
    InterfaceStorageService,
    InterfaceTaskUpdateViewService,
    InterfacePermissionService,
    InterfaceEventService,
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

    def create_count_event(self) -> InterfaceEventService:
        return EventService(CameraRepository(), CountEventRepository())

    def create_storage(self) -> InterfaceStorageService:
        return StorageServices(StorageRepository(), StorageTodayRepository())

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
