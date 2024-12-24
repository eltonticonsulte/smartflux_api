# -*- coding: utf-8 -*-
from src.services.auth_service import AuthServices
from src.interfaces import InterfaceAuthController


class AuthController(InterfaceAuthController):
    def __init__(self, services: AuthServices):
        self.services = services

    def login(self, user_name: str, password: str):
        return self.services.auth_user(user_name, password)

    def current_user(self, token: str):
        return self.services.get_current_user(token)

    def validate_token(self, token: str):
        return self.services.get_current_user(token)
