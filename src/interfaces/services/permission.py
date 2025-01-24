# -*- coding: utf-8 -*-
from abc import abstractmethod
from src.dto import ResponsePermission, RequestCreatePermission


class InterfacePermissionService:
    @abstractmethod
    def create(self, request: RequestCreatePermission) -> int:
        raise NotImplementedError("Method not implemented")
