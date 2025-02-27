# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.executors.pool import ThreadPoolExecutor
# from apscheduler.triggers.cron import CronTrigger
from src.database import DBConnectionHandler
from src.api import base_ruter
from core import get_settings
from .factory_service import FactoryService

# executors = {
#    "default": ThreadPoolExecutor(5),  # Até 5 tarefas em paralelo
# }
# scheduler = BackgroundScheduler(executors=executors)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan Iniciando scheduler...")
    try:
        with DBConnectionHandler() as db:
            print("Conexão ao banco de dados estabelecida.")
    except Exception as e:
        print(f"Erro ao estabelecer conexão ao banco de dados: {e}")
    # scheduler.start()

    yield
    # scheduler.shutdown()
    print("Scheduler finalizado.")


def event():
    print("event scheduler...")
    task = FactoryService().create_task_update_view()
    task.update_view()


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
    # trigger = CronTrigger(
    #    hour=0,
    #    minute=0,
    # )
    # scheduler.add_job(event, trigger, max_instances=1)

    return app
