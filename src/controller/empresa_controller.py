# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..common import ExceptionUserNameExists

from ..dto import EmpresaDTO
from ..services import EmpresaServices, UserServices


class EmpresaController:
    def __init__(self, empresa_services: EmpresaServices):
        self.log = logging.getLogger(__name__)
        self.router = APIRouter(prefix="/empresa", tags=["Empresa"])
        self.setup_routes()
        self.empresa_repository: EmpresaServices = empresa_services

    def setup_routes(self):
        # self.router.add_api_route("/all", self.get_users, methods=["GET"])
        # self.router.add_api_route("/{user_id}", self.get_user_by_id, methods=["GET"])
        self.router.add_api_route("/create", self.create, methods=["POST"])
        self.router.add_api_route("/login", self.get_login, methods=["POST"])
        self.router.add_api_route("/all", self.get_all, methods=["GET"])
        # self.router.add_api_route("/{user_id}", self.update_user, methods=["PUT"])
        # self.router.add_api_route("/{empresa_id}", self.delete_empresa, methods=["DELETE"])

    async def create(
        self,
        name_empresa: str,
        current_user: str = Depends(UserServices.get_current_user),
    ):

        try:
            self.empresa_repository.create_empresa(name_empresa)
        except ExceptionUserNameExists as error:
            self.log.critical(error)
            raise HTTPException(422, detail=error)
        except Exception as error:
            self.log.critical(error)
            raise HTTPException(500, detail=error)

    async def get_login(self, from_data: OAuth2PasswordRequestForm = Depends()):
        try:
            self.empresa_repository.get_login(from_data.username)
        except ExceptionUserNameExists as error:
            self.log.critical(error.messge)
            raise HTTPException(422, detail=error.messge)
        except Exception as error:
            self.log.critical(error.messge)
            raise HTTPException(404, detail=error.messge)

    async def get_all(self, current_user: str = Depends(UserServices.get_current_user)):
        try:
            return self.user_repository.get_all()
        except Exception as error:
            self.log.critical(error.messge)
            raise HTTPException(422, detail=error.messge)
