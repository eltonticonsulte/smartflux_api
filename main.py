# -*- coding: utf-8 -*-
import logging
import os
from fastapi import FastAPI

from src.controller import (
    EmpresaController,
    UserController,
    CounterEventController,
    FilialController,
)

from src.services import UserServices, EmpresaServices, FilialServices
from src.repository import UserRepository, EmpresaRepository, FilialRepository
from utils import LoggerConfig

__version__ = "0.0.0"
os.environ["__VERSION__"] = __version__

LoggerConfig()

log = logging.getLogger("smartflux_api")
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("multipart").setLevel(logging.ERROR)

from api import api_router
from core import get_settings


app = FastAPI(title=get_settings().PROJECT_NAME, version=__version__)

user_repository = UserRepository()
user_services = UserServices(user_repository)
admin_controller = UserController(user_services)
app.include_router(admin_controller.router, prefix="/api")

empresa_repository = EmpresaRepository()
empresa_service = EmpresaServices(empresa_repository)
empresa_controller = EmpresaController(empresa_service)
app.include_router(empresa_controller.router, prefix="/api")

filial_repository = FilialRepository()
filial_service = FilialServices(filial_repository)
filial_controller = FilialController(filial_service)
app.include_router(filial_controller.router, prefix="/api")

visitor_controller = CounterEventController()
app.include_router(visitor_controller.router, prefix="/api")

# app.include_router(api_router, prefix="/api")
log.info(f"smartflux_api version: {__version__}")


@app.get("/")
async def get():
    return {"status": True, "message": "SmartFlux API IA", "version": __version__}
