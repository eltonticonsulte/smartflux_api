# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from ..common import ExceptionUserNameExists

from ..dto import EmpresaDTO
from ..services import FilialServices, UserServices


class FilialController:
    def __init__(self, filal_services: FilialServices):
        self.log = logging.getLogger(__name__)
        self.router = APIRouter(prefix="/filial", tags=["Filal"])
        self.setup_routes()
        self.filial_services: FilialServices = filal_services

    def setup_routes(self):
        self.router.add_api_route(
            "/create",
            self.create,
            methods=["POST"],
            dependencies=[Depends(UserServices.get_current_user)],
        )
        self.router.add_api_route("/login", self.get_login, methods=["POST"])
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
        name: str,
        cnpj: str,
        empresa_id: int,
        current_user: str = Depends(UserServices.get_current_user),
    ):
        try:
            id_filial = self.filial_services.create(name, cnpj, empresa_id)
            return JSONResponse(status_code=201, content={"id_filial": id_filial})
        except ExceptionUserNameExists as error:
            self.log.critical(error)
            raise HTTPException(422, detail=error)
        except Exception as error:
            self.log.critical(error)
            raise HTTPException(500, detail=error)

    async def get_all(self, current_user: str = Depends(UserServices.get_current_user)):
        try:
            result = self.filial_services.get_all()

            return JSONResponse(status_code=200, content=result)
        except Exception as error:
            self.log.critical(error)
            raise HTTPException(422, detail=error)

    async def get_login(self, from_data: OAuth2PasswordRequestForm = Depends()):
        token =  self.filial_services.auth(from_data.username, from_data.password)
        if token:
            return JSONResponse(
                status_code=200, content={"access_token": token, "token_type": "bearer"}
            )

        self.log.critical("Usuario ou senhna invalida")
        raise HTTPException(422, detail="Usuario ou senhna invalida")
