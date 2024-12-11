# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from ..services import UserServices


class UserController:
    def __init__(self, user_services: UserServices):
        self.log = logging.getLogger(__name__)
        self.router = APIRouter(prefix="/auth", tags=["Auth"])
        self.setup_routes()

        self.user_services = user_services

    def setup_routes(self):
        self.router.add_api_route("/login", self.get_login, methods=["POST"])
        self.router.add_api_route("/create-user", self.create_user, methods=["POST"])

    async def get_login(self, from_data: OAuth2PasswordRequestForm = Depends()) -> dict:
        token = self.user_services.auth_user(from_data.username, from_data.password)

        if token:
            return JSONResponse(
                status_code=200, content={"access_token": token, "token_type": "static"}
            )

        self.log.critical("Usuario ou senhna invalida")
        raise HTTPException(422, detail="Usuario ou senhna invalida")

    async def create_user(
        self, current_user: str = Depends(UserServices.get_current_user)
    ):
        self.log.debug(f"current_user {current_user}")
        return {"message": "Authenticated", "user": current_user}
