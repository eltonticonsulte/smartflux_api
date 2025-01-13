# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import List
from src.dto import (
    AuthUserRequest,
    AuthUserResponse,
    CreateUserRequest,
    UserPermissionAccessDTO,
)


class InterfaceUserService(ABC):
    @abstractmethod
    def auth_user(self, request: AuthUserRequest) -> AuthUserResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def current_user(self, token: str) -> UserPermissionAccessDTO:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def create(self, request: CreateUserRequest) -> AuthUserResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all(self) -> List[AuthUserResponse]:
        raise NotImplementedError("Method not implemented")
