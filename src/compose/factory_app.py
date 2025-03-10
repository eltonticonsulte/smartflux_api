# -*- coding: utf-8 -*-
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from src.database import DBConnectionHandler
from src.interfaces import IAdapterTask
from src.api import base_ruter
from core import get_settings
from .factory_service import FactoryService

executors = {
    "default": ThreadPoolExecutor(5),  # Até 5 tarefas em paralelo
}
scheduler = BackgroundScheduler(executors=executors)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan Iniciando scheduler...")
    try:
        with DBConnectionHandler() as db:
            print("Conexão ao banco de dados estabelecida.")
    except Exception as e:
        print(f"Erro ao estabelecer conexão ao banco de dados: {e}")
    scheduler.start()

    yield
    scheduler.shutdown()
    print("Scheduler finalizado.")


def event_process_max_ocupation():
    print("event scheduler...")
    task: IAdapterTask = FactoryService().create_task_compute_max_ocupation()
    task.process()


def permsion(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permite qualquer origem
        allow_credentials=True,
        allow_methods=["*"],  # Permite qualquer método (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],  # Permite qualquer cabeçalho
    )


def create_app(log, version):

    app = FastAPI(title=get_settings().PROJECT_NAME, version=version, lifespan=lifespan)
    app.include_router(base_ruter, prefix=get_settings().API_V1_STR)
    permsion(app)
    trigger = CronTrigger(
        minute="*/10",
    )
    scheduler.add_job(event_process_max_ocupation, trigger, max_instances=1)

    return app
