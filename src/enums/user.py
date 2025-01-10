# -*- coding: utf-8 -*-
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    EMPRESA = "empresa"
    FILIAL = "filial"
