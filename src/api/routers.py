# -*- coding: utf-8 -*-
from fastapi import APIRouter

from src.controllers.user import router as user_route
from src.controllers.empresa import router as empresa_route
from src.controllers.filial import router as filial_route
from src.controllers.camera import router as camera_route
from src.controllers.visitor import router as visitor_route
from src.controllers.event_count import router as router_event_count
from src.controllers.aplication import router as router_aplication
from src.controllers.permission import router as router_permission

base_ruter = APIRouter()

base_ruter.include_router(user_route, prefix="/user", tags=["Usuario"])
base_ruter.include_router(
    router_permission, prefix="/permission", tags=["Permissão de usuário"]
)
base_ruter.include_router(empresa_route, prefix="/empresa", tags=["Empresa"])
base_ruter.include_router(filial_route, prefix="/filial", tags=["Filial"])

base_ruter.include_router(camera_route, prefix="/camera", tags=["Camera"])


base_ruter.include_router(router_event_count, prefix="/event", tags=["Eventos"])
base_ruter.include_router(visitor_route, prefix="/visitor", tags=["Visitor"])


base_ruter.include_router(router_aplication, prefix="/aplication", tags=["Aplication"])
