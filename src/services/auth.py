# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import hmac
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from core import get_settings
from ..database import DataUserDB, DBConnectionHandler
from ..repository import UserRepository
from ..common import UserRole
from ..dto import userDTO
from ..mappers import UserMapper

auth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


class AuthServices:
    def __init__(self):
        self.data_base = UserRepository()

    def create_user(self, user: userDTO) -> bool:
        if self.data_base.get_user_by_name(user.username):
            return False
        self.data_base.create_user(user)
        return True

    def auth_user(self, user_name: str, password: str) -> bool:
        self.log.debug(f"get_login {user_name}")
        hash_password: str = self.data_base.get_user_by_name(user_name)
        if not hash_password:
            return False
        return hmac.compare_digest(
            hash_password.encode("utf-8"), password.encode("utf-8")
        )

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
