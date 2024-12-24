# -*- coding: utf-8 -*-
import logging
from typing_extensions import Annotated, Doc

from fastapi import Form
from src.repository import AuthRepository
from src.services import AuthServices
from controller.auth_controller import AuthController


class AuthComposer:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.repository = AuthRepository()
        self.service = AuthServices(self.repository)
        self.controller = AuthController(self.service)

    @staticmethod
    def current_user(token: str):
        return AuthServices.get_current_user(token)


class AuthComposerLogin(AuthComposer):
    def __init__(
        self,
        *,
        username: Annotated[
            str,
            Form(),
            Doc("username string requeired for authentication"),
        ],
        password: Annotated[
            str,
            Form(),
            Doc("password string requeired for authentication"),
        ]
    ):
        super().__init__()
        self.username = username
        self.password = password

    def get_token(self) -> str:
        return self.controller.login(self.username, self.password)
