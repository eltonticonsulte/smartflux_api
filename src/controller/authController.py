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
        self.auth = AuthServices()

    def setup_routes(self):
        self.router.add_api_route("/login", self.get_login, methods=["POST"])
        self.router.add_api_route("/protected", self.protected_route, methods=["GET"])
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

        if from_data.username != "admin":
            self.log.critical("Usuario ou senhna invalida")
            raise HTTPException(422, detail="Usuario ou senhna invalida")
        if from_data.password != "admin123":
            self.log.critical("Usuario ou senhna invalida")
            raise HTTPException(422, detail="Usuario ou senhna invalida")
        token = self.create_access_token(data={"sub": from_data.username})
        return {"access_token": token, "token_type": "bearer"}

    async def get_current_user(self, token: str = Depends(auth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return username

    async def protected_route(self, current_user: str = Depends(get_current_user)):
        return {"message": "Authenticated", "user": current_user}
