# -*- coding: utf-8 -*-
import logging
import os
from fastapi import FastAPI
from utils import LoggerConfig

__version__ = "0.0.0"
os.environ["VERSION"] = __version__

LoggerConfig()

log = logging.getLogger("smartflux_api")
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("multipart").setLevel(logging.ERROR)

from api import api_router
from core import settings


app = FastAPI(title=settings.TITLE, version=__version__)
app.include_router(api_router, prefix="/api")
log.info(f"smartflux_api version: {__version__}")


@app.get("/")
async def get():
    return {"status": True, "message": "Redsoft API IA", "version": __version__}
