# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError
from .connect import DBConnectionHandler
from .schema import (
    Filial,
    Camera,
    Zone,
    EventCountTemp,
    EventCountHourly,
    Empresa,
    UserRole,
    Usuario,
)
