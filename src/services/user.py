# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import logging
import hmac
from jose import JWTError, jwt
from core import get_settings
from src.repository import UserRepository
from src.database import Usuario
from src.exceptions import ServiceUserExecption, ServiceUserJwtExecption
from src.dto import (
    ResponseAuthUser,
    RequestCreateUser,
    RequestAuthUser,
    UserPermissionAccessDTO,
)
from src.mappers import UserMapper
from src.interfaces import InterfaceUserService


class UserServices(InterfaceUserService):
    def __init__(self, repo_user: UserRepository):
        self.repo_user = repo_user
        self.log = logging.getLogger(__name__)

    def create(self, user: RequestCreateUser) -> int:
        self.log.debug(f"create_user {user}")
        entity = UserMapper.create_user_to_entity(user)
        user_id = self.repo_user.create(entity)
        new_user = self.repo_user.get_by_id(user_id)
        return UserMapper.get_entity_to_response(new_user)

    def auth_user(self, request: RequestAuthUser) -> ResponseAuthUser:
        password_hash = UserMapper.password_to_hash(request.password)
        user: Usuario = self.repo_user.get_user_by_name(request.username)
        self.log.debug(f"auth_user {user}")

        if not user:
            raise ServiceUserExecption("User not found")
        if not self.__compare_hash(user.password_hash, password_hash):
            raise ServiceUserExecption("Invalid credentials")
        if not user.is_active:
            raise ServiceUserExecption("Inactive user")

        user_result = ResponseAuthUser(
            username=user.username,
            user_id=user.user_id,
            access_token="",
            token_type="bearer",
            is_active=user.is_active,
            role=user.role,
        )
        UserServices.create_access_token(user_result)

        return user_result

    def __compare_hash(self, hash1: str, hash2: str) -> bool:
        return hmac.compare_digest(hash1.encode("utf-8"), hash2.encode("utf-8"))

    def current_user(self, token: str) -> UserPermissionAccessDTO:
        try:
            payload = jwt.decode(
                token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise ServiceUserExecption("User Invalid")
            user = self.repo_user.get_user_by_name(username)
            permission = self.repo_user.fetch_permisso_by_user(user.user_id)
            self.log.debug(f"current_user {user} {permission}")

            return UserMapper.to_permissao(user, permission)
        except JWTError as erros:
            raise ServiceUserJwtExecption(f"JWT Error: {erros}") from erros

    @staticmethod
    def create_access_token(user: RequestAuthUser) -> None:
        to_encode = {"sub": user.username}
        expire = datetime.utcnow() + timedelta(
            minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({"exp": expire})
        result_token = jwt.encode(
            to_encode, get_settings().SECRET_KEY, algorithm=get_settings().ALGORITHM
        )
        user.access_token = result_token

    def get_all(self):
        all_users = self.repo_user.get_all()
        return [UserMapper.get_entity_to_response(user) for user in all_users]
