# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import HTTPException
import logging
from ..repository import userRepository, ExceptionUserNameExists
from ..validator import userValidator
from ..entity import UserReciver


class AdminController:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.router = APIRouter(prefix="/admin", tags=["Admin"])
        self.setup_routes()
        self.user_repository = userRepository()

    def setup_routes(self):
        self.router.add_api_route("/login", self.get_login, methods=["POST"])

    async def get_login(self, user: UserReciver):

        if user.username != "admin":
            self.log.critical("Usuario ou senhna invalida")
            raise HTTPException(422, detail="Usuario ou senhna invalida")
        if user.password != "admin123":
            self.log.critical("Usuario ou senhna invalida")
            raise HTTPException(422, detail="Usuario ou senhna invalida")

        return f"tokoen admin"
