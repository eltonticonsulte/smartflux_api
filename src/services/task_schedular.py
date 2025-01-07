# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

executors = {
    "default": ThreadPoolExecutor(5),
}
scheduler = BackgroundScheduler(executors=executors)


def start_scheduler():
    if not scheduler.running:
        scheduler.start()


def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()


def exemplo_tarefa():
    print("Tarefa executada!")


scheduler.add_job(exemplo_tarefa, "interval", minutes=1)
