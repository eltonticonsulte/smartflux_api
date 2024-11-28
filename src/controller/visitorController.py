# -*- coding: utf-8 -*-
from fastapi import APIRouter
from ..entity.visitorEntity import PullEventReciver
from ..validator import VisitorValidate


class VisitorController:
    def __init__(self):
        self.router = APIRouter(prefix="/visitor", tags=["Visitors"])
        self.setup_routes()
        self.validator = VisitorValidate()

    def setup_routes(self):
        self.router.add_api_route("/all", self.get_users, methods=["GET"])
        self.router.add_api_route("/register", self.register_event, methods=["POST"])

    async def get_users(self):
        pass

    async def register_event(self, data: PullEventReciver):
        self.validator.validate(data)
        print(data)
