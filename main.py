# -*- coding: utf-8 -*-
import logging
import os
from fastapi import FastAPI

from src.controller import userController, visitorController
from utils import LoggerConfig

__version__ = "0.0.0"
os.environ["__VERSION__"] = __version__

LoggerConfig()

log = logging.getLogger("smartflux_api")
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("multipart").setLevel(logging.ERROR)

from api import api_router
from core import settings


app = FastAPI(title=settings.TITLE, version=__version__)

user_controller = userController.UserController()
app.include_router(user_controller.router, prefix="/api")

visitor_controller = visitorController.VisitorController()
app.include_router(visitor_controller.router, prefix="/api")

# app.include_router(api_router, prefix="/api")
log.info(f"smartflux_api version: {__version__}")


@app.get("/")
async def get():
    return {"status": True, "message": "Redsoft API IA", "version": __version__}
