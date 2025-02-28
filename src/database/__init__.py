# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError
from .connect import DBConnectionHandler
from .schema import (
    Filial,
    Camera,
    EventCountTemp,
    EventCount,
    Empresa,
    UserRule,
    Usuario,
    PermissaoAcesso,
    CountMaximunCapacity,
    WebsocketNotification,
)
