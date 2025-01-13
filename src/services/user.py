# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import logging
import hmac
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core import get_settings
from ..repository import UserRepository, PermissaoRepository
from ..database import Usuario
from ..enums import UserRole
from ..dto import AuthUserResponse, CreateUserRequest, AuthUserRequest, GetUserResponse
from ..mappers import UserMapper
from ..interfaces import InterfaceUserService

auth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/login")


class ServiceUserExecption(Exception):
    def __init__(self, message):
        self.message = message


class UserServices(InterfaceUserService):
    def __init__(self, repo_user: UserRepository, repo_permissao: PermissaoRepository):
        self.repo_user = repo_user
        self.repo_permissao = repo_permissao
        self.log = logging.getLogger(__name__)

    def create(self, user: CreateUserRequest) -> int:
        self.log.debug(f"create_user {user}")
        entity = UserMapper.create_user_to_entity(user)
        user_id = self.repo_user.create(entity)
        new_user = self.repo_user.get_by_id(user_id)
        return UserMapper.get_entity_to_response(new_user)

    def auth_user(self, request: AuthUserRequest) -> AuthUserResponse:
        password_hash = UserMapper.password_to_hash(request.password)
        user: Usuario = self.repo_user.get_user_by_name(request.username)
        self.log.debug(f"auth_user {user}")

        if not user:
            raise ServiceUserExecption("User not found")
        if not self.__compare_hash(user.password_hash, password_hash):
            raise ServiceUserExecption("Invalid credentials")
        if not user.is_active:
            raise ServiceUserExecption("Inactive user")

        user_result = AuthUserResponse(
            username=user.username,
            access_token="gdfff",
            token_type="bearer",
            role=user.role,
        )
        self.log.critical(user_result)
        UserServices.create_access_token(user_result)

        return user_result

    def __compare_hash(self, hash1: str, hash2: str) -> bool:
        return hmac.compare_digest(hash1.encode("utf-8"), hash2.encode("utf-8"))

    def current_user(self, token: str) -> GetUserResponse:
        try:
            payload = jwt.decode(
                token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise ServiceUserExecption("User Invalid")
            user = self.repo_user.get_user_by_name(username)
            return UserMapper.get_entity_to_response(user)
        except JWTError as erros:
            raise ServiceUserExecption(f"JWT Error: {erros}") from erros

    @staticmethod
    def create_access_token(user: AuthUserRequest) -> None:
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
