# -*- coding: utf-8 -*-
from fastapi import FastAPI
from src.database import DBConnectionHandler
from src.api import base_ruter
from core import get_settings
from ..services import start_scheduler, shutdown_scheduler


def create_app(log, version):

    app = FastAPI(title=get_settings().PROJECT_NAME, version=version)
    app.include_router(base_ruter, prefix="/api")

    @app.on_event("startup")
    def startup_event():
        with DBConnectionHandler() as session:
            log.info(f"Connected to database: {get_settings().view_connection}")
        start_scheduler()

    @app.on_event("shutdown")
    def shutdown_event():
        shutdown_scheduler()

    return app
