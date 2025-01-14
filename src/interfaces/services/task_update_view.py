# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from src.repository import (
    TaskUpdateViewRepository,
    CountEventStorageRepository,
    TodayEstorageRepository,
)


class InterfaceTaskUpdateViewService(ABC):
    @abstractmethod
    def update_view(
        self,
        repo_view: TaskUpdateViewRepository,
        repo_storage: CountEventStorageRepository,
        repo_event: TodayEstorageRepository,
    ) -> None:
        raise NotImplementedError("Method not implemented")
