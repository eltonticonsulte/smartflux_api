# -*- coding: utf-8 -*-
from fastapi import APIRouter
from ..repository import userRepository
from ..validator import userValidator


class UserController:
    def __init__(self):
        self.router = APIRouter(prefix="/user", tags=["Users"])
        self.setup_routes()
        self.user_repository = userRepository()

    def setup_routes(self):
        self.router.add_api_route("/all", self.get_users, methods=["GET"])
        self.router.add_api_route("/{user_id}", self.get_user_by_id, methods=["GET"])
        self.router.add_api_route("/create", self.create_user, methods=["POST"])
        self.router.add_api_route("/{user_id}", self.update_user, methods=["PUT"])
        self.router.add_api_route("/{user_id}", self.delete_user, methods=["DELETE"])

    async def get_users(self):
        print("get_users")
        self.user_repository.get_all_user()

    async def create_user(self, name: str):
        print("create_user", name)

    async def get_user_by_id(self, name: str):
        pass

    async def update_user(self, name: str):
        pass

    async def delete_user(self, name: str):
        pass
