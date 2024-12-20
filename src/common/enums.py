# -*- coding: utf-8 -*-
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    EMPRESA = "empresa"
    FILIAL = "filial"


class CameraState(Enum):
    RUNING = 0
    STOP = 2
    ERROR = 3
