# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import HTTPException, status, Depends
import logging
from core import get_settings
from fastapi_sessions.backends.implementations import InMemoryBackend
from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..repository import UserRepository, ExceptionUserNameExists
from ..services import UserServices, auth2_scheme


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
        if self.user_services.auth_user(from_data.username, from_data.password):
            token = UserServices.create_access_token(data={"sub": from_data.username})
            return {"access_token": token, "token_type": "bearer"}

        self.log.critical("Usuario ou senhna invalida")
        raise HTTPException(422, detail="Usuario ou senhna invalida")

    async def create_user(
        self, current_user: str = Depends(UserServices.get_current_user)
    ):
        self.log.debug(f"current_user {current_user}")
        return {"message": "Authenticated", "user": current_user}
