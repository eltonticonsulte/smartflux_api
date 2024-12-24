# -*- coding: utf-8 -*-
from fastapi import APIRouter, Header
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceAuthController, InterfaceFilialController
from .core import auth2_admin, controller_auth, controller_filial


router = APIRouter()


class CreateFilialData(BaseModel):
    name_filial: str
    empresa_id: int
    cnpj: str


@router.post("/create")
async def create(
    data: CreateFilialData,
    token: str = Depends(auth2_admin),
    controller: InterfaceFilialController = Depends(controller_filial),
    controller_auth: InterfaceAuthController = Depends(controller_auth),
):
    try:
        controller_auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        id_filial = controller.create(data.name_filial, data.empresa_id, data.cnpj)
        return JSONResponse(status_code=201, content={"id_filial": id_filial})
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.post("/Auth")
async def get_login(
    token: str = Header(...),
    controller: InterfaceAuthController = Depends(controller_auth),
):
    try:
        controller.auth(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        return JSONResponse(
            status_code=200,
            content={"access_token": token, "token_type": "bearer"},
        )
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/all")
async def get_all(
    token: str = Depends(auth2_admin),
    controller: InterfaceFilialController = Depends(controller_filial),
    controller_auth: InterfaceAuthController = Depends(controller_auth),
):
    try:
        controller_auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result = controller.get_all()
        return JSONResponse(status_code=200, content=result)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
