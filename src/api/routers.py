# -*- coding: utf-8 -*-
from fastapi import APIRouter

from ..controllers.user import router as user_route
from ..controllers.empresa import router as empresa_route
from ..controllers.filial import router as filial_route
from ..controllers.zone import router as zone_route
from ..controllers.camera import router as camera_route
from ..controllers.count_event import router as count_event
from ..controllers.count_event_storage import router as count_event_storage
from ..controllers.aplication import router as router_aplication

base_ruter = APIRouter()
base_ruter.include_router(user_route, prefix="/user", tags=["Usuario"])
base_ruter.include_router(empresa_route, prefix="/empresa", tags=["Empresa"])
base_ruter.include_router(filial_route, prefix="/filial", tags=["Filial"])

base_ruter.include_router(zone_route, prefix="/zone", tags=["Zona"])
base_ruter.include_router(camera_route, prefix="/camera", tags=["Camera"])

base_ruter.include_router(count_event, prefix="/event", tags=["Eventos"])

base_ruter.include_router(
    count_event_storage, prefix="/storage", tags=["Eventos Storage"]
)
base_ruter.include_router(router_aplication, prefix="/aplication", tags=["Aplication"])
