# -*- coding: utf-8 -*-
import logging
import os
from fastapi import FastAPI
from utils import LoggerConfig
from core import get_settings
from src.database import DBConnectionHandler
from src.compose import create_app

__version__ = "0.0.11"
os.environ["__VERSION__"] = __version__

LoggerConfig()


log = logging.getLogger("smartflux_api")
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("python_multipart").setLevel(logging.ERROR)

app = create_app(log, __version__)


log.info(f"smartflux_api version: {__version__}")


@app.get("/")
async def get():
    return {"status": True, "message": "SmartFlux API IA", "version": __version__}
