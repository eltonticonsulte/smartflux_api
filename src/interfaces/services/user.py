# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from src.dto import AuthUserRequest, AuthUserResponse


class InterfaceUserService(ABC):
    @abstractmethod
    def auth_user(self, request: AuthUserRequest) -> AuthUserResponse:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def current_user(self, token: str):
        raise NotImplementedError("Method not implemented")
