# -*- coding: utf-8 -*-
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    USER_EMPRESA = "empresa"
    USER_FILIAL = "filial"
