# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import HTTPException
import logging
from ..repository import userRepository, ExceptionUserNameExists
from ..validator import userValidator
from ..entity import UserReciver


class UserController:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.router = APIRouter(prefix="/user", tags=["Users"])
        self.setup_routes()
        self.user_repository = userRepository()

    def setup_routes(self):
        # self.router.add_api_route("/all", self.get_users, methods=["GET"])
        # self.router.add_api_route("/{user_id}", self.get_user_by_id, methods=["GET"])
        self.router.add_api_route("/create", self.create_user, methods=["POST"])
        self.router.add_api_route("/login", self.get_login, methods=["POST"])
        # self.router.add_api_route("/{user_id}", self.update_user, methods=["PUT"])
        # self.router.add_api_route("/{user_id}", self.delete_user, methods=["DELETE"])

    async def create_user(self, user: UserReciver):
        try:
            self.user_repository.create_user(user)
        except ExceptionUserNameExists as error:
            self.log.critical(error.messge)
            raise HTTPException(422, detail=error.messge)

    async def get_login(self, user: UserReciver):
        try:
            self.user_repository.get_login(user)
        except ExceptionUserNameExists as error:
            self.log.critical(error.messge)
            raise HTTPException(422, detail=error.messge)
