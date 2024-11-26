# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from fastapi import APIRouter

from api.user import router_user
from api.event import router_event_counter
from api.device import router_device
from api.cliente import router_client

api_router = APIRouter()

api_router.include_router(router_user, prefix="/v1", tags=["User"])
api_router.include_router(router_event_counter, prefix="/v1", tags=["Evento"])
api_router.include_router(router_device, prefix="/v1", tags=["Cameras"])
api_router.include_router(router_client, prefix="/v1", tags=["Cliente"])
