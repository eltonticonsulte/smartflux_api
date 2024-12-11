# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from ..common import ExceptionUserNameExists

from ..dto import EmpresaDTO
from ..services import EmpresaServices, UserServices


class EmpresaController:
    def __init__(self, empresa_services: EmpresaServices):
        self.log = logging.getLogger(__name__)
        self.router = APIRouter(prefix="/empresa", tags=["Empresa"])
        self.setup_routes()
        self.empresa_services: EmpresaServices = empresa_services

    def setup_routes(self):
        self.router.add_api_route(
            "/create",
            self.create,
            methods=["POST"],
            dependencies=[Depends(UserServices.get_current_user)],
        )
        # self.router.add_api_route("/login", self.get_login, methods=["POST"])
        self.router.add_api_route(
            "/all",
            self.get_all,
            methods=["GET"],
            dependencies=[Depends(UserServices.get_current_user)],
        )
        # self.router.add_api_route("/{user_id}", self.update_user, methods=["PUT"])
        # self.router.add_api_route("/{empresa_id}", self.delete_empresa, methods=["DELETE"])

    async def create(
        self,
        name_empresa: str,
        current_user: str = Depends(UserServices.get_current_user),
    ):
        try:
            id_empresa = self.empresa_services.create_empresa(name_empresa)
            return JSONResponse(status_code=201, content={"id_empresa": id_empresa})
        except ExceptionUserNameExists as error:
            self.log.critical(error)
            raise HTTPException(422, detail=error)
        except Exception as error:
            self.log.critical(error)
            raise HTTPException(500, detail=error)

    async def get_all(self, current_user: str = Depends(UserServices.get_current_user)):
        try:
            result = self.empresa_services.get_all()

            return JSONResponse(status_code=200, content=result)
        except Exception as error:
            self.log.critical(error)
            raise HTTPException(422, detail=error)
