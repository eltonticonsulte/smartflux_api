# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import (
    RequestAuthUser,
    ResponseAuthUser,
    RequestCreateUser,
    UserPermissionAccessDTO,
)


class InterfaceUserService(ABC):
    @abstractmethod
    def auth_user(self, request: RequestAuthUser) -> ResponseAuthUser:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def current_user(self, token: str) -> UserPermissionAccessDTO:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create(self, request: RequestCreateUser) -> ResponseAuthUser:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[ResponseAuthUser]:
        raise NotImplementedError("Method not implemented")
