# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import logging
import hmac
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from core import get_settings
from ..database import DBConnectionHandler
from ..repository import UserRepository
from ..common import UserRole
from ..dto import UserDTO
from ..mappers import UserMapper

auth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


class UserServices:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.log = logging.getLogger(__name__)

    def create_user(self, user: UserDTO) -> bool:
        data_user: UserDTO = self.user_repository.get_user_by_name(user.username)
        if data_user.username != "":
            raise ValueError("User name already exists")

        return self.user_repository.create_user(user)

    def auth_user(self, user_name: str, password: str) -> bool:
        user_input = UserDTO(username=user_name, password=password)
        user_input = UserMapper.to_entity(user_input)
        user: UserDTO = self.user_repository.get_user_by_name(user_name)
        if user.username == "":
            raise ValueError("User not exists")
        if not user.is_active:
            raise ValueError("User not active")
        if self.__compare_hash(user.hash_password, user_input.password_hash):
            return UserServices.create_access_token(data={"sub": user_name})

    def __compare_hash(self, hash1: str, hash2: str) -> bool:
        return hmac.compare_digest(hash1.encode("utf-8"), hash2.encode("utf-8"))

    @staticmethod
    def get_current_user(token: str = Depends(auth2_scheme)):

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
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM
        )
