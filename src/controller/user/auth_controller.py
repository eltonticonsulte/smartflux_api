# -*- coding: utf-8 -*-
from src.services.auth_service import AuthServices


class AuthController:
    def __init__(self, auth_services: AuthServices):
        self.auth_services = auth_services

    def login(self, user_name: str, password: str):
        return self.auth_services.auth_user(user_name, password)
