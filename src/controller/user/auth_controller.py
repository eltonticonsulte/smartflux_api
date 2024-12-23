# -*- coding: utf-8 -*-
from src.services.auth_service import AuthServices


class AuthController:
    def __init__(self, services: AuthServices):
        self.services = services

    def login(self, user_name: str, password: str):
        return self.services.auth_user(user_name, password)
