# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import HTTPException, status, Depends
import logging
from core import get_settings
from fastapi_sessions.backends.implementations import InMemoryBackend
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..repository import userRepository, ExceptionUserNameExists
from ..entity import UserReciver
from ..services import AuthServices, auth2_scheme


class AuthController:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.router = APIRouter(prefix="/auth", tags=["Auth"])
        self.setup_routes()
        self.user_repository = userRepository()

    def setup_routes(self):
        self.router.add_api_route("/login", self.get_login, methods=["POST"])
        self.router.add_api_route("/create-user", self.create_user, methods=["POST"])

        # self.router.add_api_route("/logget", self.get_current_user, methods=["GET"])

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM
        )

    async def get_login(self, from_data: OAuth2PasswordRequestForm = Depends()):
        # self.user_repository.get_login(user, password)

        if from_data.username != "admin":
            self.log.critical("Usuario ou senhna invalida")
            raise HTTPException(422, detail="Usuario ou senhna invalida")
        if from_data.password != "admin123":
            self.log.critical("Usuario ou senhna invalida")
            raise HTTPException(422, detail="Usuario ou senhna invalida")
        token = self.create_access_token(data={"sub": from_data.username})
        return {"access_token": token, "token_type": "bearer"}

    async def create_user(
        self, current_user: str = Depends(AuthServices.get_current_user)
    ):
        self.log.debug(f"current_user {current_user}")
        return {"message": "Authenticated", "user": current_user}
