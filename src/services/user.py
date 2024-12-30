# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import logging
import hmac
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core import get_settings
from ..repository import UserRepository
from ..database import Usuario
from ..dto import (
    AuthUserResponse,
    CreateUserRequest,
    CreateUserResponse,
    AuthUserRequest,
)
from ..mappers import UserMapper
from ..interfaces import InterfaceUserService

auth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/login")


class ServiceUserExecption(Exception):
    def __init__(self, message):
        self.message = message


class UserServices(InterfaceUserService):
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def create(self, user: CreateUserRequest) -> int:
        entity = UserMapper.create_user_to_entity(user)
        self.repository.create(entity)
        return CreateUserResponse(username=user.username)

    def auth_user(self, request: AuthUserRequest) -> AuthUserResponse:
        password_hash = UserMapper.password_to_hash(request.password)
        user: Usuario = self.repository.get_user_by_name(request.username)
        self.log.debug(f"auth_user {user}")
        if not user:
            raise ServiceUserExecption("User not found")
        if not self.__compare_hash(user.password_hash, password_hash):
            raise ServiceUserExecption("Invalid credentials")
        if not user.is_active:
            raise ServiceUserExecption("Inactive user")

        new_token = UserServices.create_access_token(request.username)

        return AuthUserResponse(
            username=user.username,
            access_token=new_token,
            token_type="bearer",
            role=user.role,
        )

    def __compare_hash(self, hash1: str, hash2: str) -> bool:
        return hmac.compare_digest(hash1.encode("utf-8"), hash2.encode("utf-8"))

    @staticmethod
    def current_user(token: str):
        try:
            payload = jwt.decode(
                token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise ServiceUserExecption("User Invalid")
        except JWTError as erros:
            raise ServiceUserExecption(f"JWT Error: {erros}")
        return username

    @staticmethod
    def create_access_token(user_name: str) -> str:
        to_encode = {"sub": user_name}
        expire = datetime.utcnow() + timedelta(
            minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM
        )
