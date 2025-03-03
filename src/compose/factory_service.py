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
    CapacityRepository,
)
from src.services import (
    CameraServices,
    UserServices,
    EmpresaServices,
    FilialServices,
    VisitorServices,
    TaskUpdateViewService,
    PermissionService,
    EventService,
)

from src.interfaces import (
    InterfaceCameraService,
    InterfaceUserService,
    InterfaceEmpresaService,
    InterfaceFilialService,
    InterfaceVisitorService,
    InterfaceTaskUpdateViewService,
    InterfacePermissionService,
    InterfaceEventService,
)
from src.interfaces import IAdapterTask

from src.tasks import TaskCapacity


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

    def create_visitor(self) -> InterfaceVisitorService:
        return VisitorServices(
            StorageRepository(), StorageTodayRepository(), CameraRepository()
        )

    def create_task_update_view(self) -> InterfaceTaskUpdateViewService:
        return TaskUpdateViewService(
            TaskUpdateViewRepository(),
            StorageRepository(),
            StorageTodayRepository(),
        )

    def create_task_compute_max_ocupation(self) -> IAdapterTask:
        print("tkas ")
        return TaskCapacity(
            CapacityRepository(), StorageTodayRepository(), FilialRepository()
        )

    def create_permission(self) -> InterfacePermissionService:
        return PermissionService(PermissionRepository())
