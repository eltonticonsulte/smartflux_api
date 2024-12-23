# -*- coding: utf-8 -*-
from fastapi import APIRouter

from .user import router as user_route
from .empresa import router as empresa_route
from .filial import router as filial_route
from .counter import router as counter_route

base_ruter = APIRouter()
base_ruter.include_router(user_route, prefix="/user", tags=["Usuario"])
base_ruter.include_router(empresa_route, prefix="/empresa", tags=["Empresa"])
base_ruter.include_router(filial_route, prefix="/filial", tags=["Filial"])
base_ruter.include_router(
    counter_route, prefix="/counter-event", tags=["Evento de contagem"]
)
