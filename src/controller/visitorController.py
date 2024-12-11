# -*- coding: utf-8 -*-
from fastapi import APIRouter, status
from ..entity.visitorEntity import PullEventReciver


class CounterEventController:
    def __init__(self):
        self.router = APIRouter(prefix="/counter-event", tags=["Evento de contagem"])
        self.setup_routes()

    def setup_routes(self):
        # self.router.add_api_route("/all", self.get_users, methods=["GET"])
        self.router.add_api_route(
            "/register",
            self.register_event,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )

    async def get_users(self):
        pass

    async def register_event(self, data: PullEventReciver):
        pass
