# -*- coding: utf-8 -*-
from abc import abstractmethod
from src.dto import PermissionResponse, CreatePermissionRequest


class InterfacePermissionService:
    @abstractmethod
    def create(self, request: CreatePermissionRequest) -> int:
        raise NotImplementedError("Method not implemented")
