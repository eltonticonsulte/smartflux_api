# -*- coding: utf-8 -*-
import logging
import os
from fastapi import FastAPI
from utils import LoggerConfig
from src import base_ruter


__version__ = "0.0.0"
os.environ["__VERSION__"] = __version__

LoggerConfig()


log = logging.getLogger("smartflux_api")
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("multipart").setLevel(logging.ERROR)

from core import get_settings

app = FastAPI(title=get_settings().PROJECT_NAME, version=__version__)
app.include_router(base_ruter, prefix="/api")

log.info(f"smartflux_api version: {__version__}")


@app.get("/")
async def get():
    return {"status": True, "message": "SmartFlux API IA", "version": __version__}
