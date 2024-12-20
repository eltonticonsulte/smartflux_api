# -*- coding: utf-8 -*-
class BaseAppException(Exception):
    """Classe base para exceções personalizadas."""


class InvalidCredentialsException(BaseAppException):
    """Exceção levantada para credenciais inválidas."""

    def __init__(self, message="Invalid username or password."):
        self.message = message
        super().__init__(self.message)


class InactiveUserException(BaseAppException):
    """Exceção levantada quando o usuário está inativo."""

    def __init__(self, message="User account is inactive."):
        self.message = message
        super().__init__(self.message)


class ExceptionUserNameExists(Exception):
    def __init__(self, username: str):
        self.messge = f"User name '{username}' already exists"
        super().__init__(self.messge)

    def __str__(self):
        return self.messge
