# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from src.repository import (
    TaskUpdateViewRepository,
    StorageRepository,
    StorageTodayRepository,
)


class InterfaceTaskUpdateViewService(ABC):
    @abstractmethod
    def update_view(
        self,
        repo_view: TaskUpdateViewRepository,
        repo_storage: StorageRepository,
        repo_event: StorageTodayRepository,
    ) -> None:
        raise NotImplementedError("Method not implemented")
