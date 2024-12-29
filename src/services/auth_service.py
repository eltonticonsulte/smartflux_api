# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import logging
import hmac
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core import get_settings
from ..repository import AuthRepository
from ..dto import UserDTO
from ..mappers import UserMapper
from ..interfaces import InterfaceAuthService

auth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/login")


class ServiceAuthExecption(Exception):
    def __init__(self, message):
        self.message = message


class AuthServices(InterfaceAuthService):
    def __init__(self, repository: AuthRepository):
        self.repository = repository
        self.log = logging.getLogger(__name__)

    def auth_user(self, user_name: str, password: str) -> str:
        password_hash = UserMapper.password_to_hash(password)
        user: UserDTO = self.repository.get_user_by_name(user_name)
        if not self.__compare_hash(user.hash_password, password_hash):
            raise ServiceAuthExecption("Invalid credentials")
        if not user.is_active:
            raise ServiceAuthExecption("Inactive user")

        return AuthServices.create_access_token(user_name)

    def __compare_hash(self, hash1: str, hash2: str) -> bool:
        return hmac.compare_digest(hash1.encode("utf-8"), hash2.encode("utf-8"))

    @staticmethod
    def current_user(token: str):

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
