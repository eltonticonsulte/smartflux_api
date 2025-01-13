# -*- coding: utf-8 -*-
from enum import Enum


class UserRole(str, Enum):
    ADMIN = 0
    EMPRESA = 1
    FILIAL = 2
