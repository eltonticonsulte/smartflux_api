# -*- coding: utf-8 -*-
from fastapi import APIRouter

from ..views.auth_view import router as user_route
from ..views.empresa_view import router as empresa_route
from ..views.filial_view import router as filial_route
from ..views.zone_view import router as zone_route
from ..views.camera_view import router as camera_route

base_ruter = APIRouter()
base_ruter.include_router(user_route, prefix="/user", tags=["Usuario"])
base_ruter.include_router(empresa_route, prefix="/empresa", tags=["Empresa"])
base_ruter.include_router(filial_route, prefix="/filial", tags=["Filial"])

base_ruter.include_router(zone_route, prefix="/zone", tags=["Zona"])
base_ruter.include_router(camera_route, prefix="/camera", tags=["Camera"])
