# -*- coding: utf-8 -*-
from fastapi import APIRouter, Header
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceAuthService, InterfaceFilialService
from .core import auth2_admin, get_controller_auth, get_controller_filial


router = APIRouter()


class CreateFilialData(BaseModel):
    name_filial: str
    empresa_id: int
    cnpj: str


@router.post("/create")
async def create(
    data: CreateFilialData = Depends(),
    token: str = Depends(auth2_admin),
    service: InterfaceFilialService = Depends(get_controller_filial),
    auth: InterfaceAuthService = Depends(get_controller_auth),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        id_filial = service.create(data.name_filial, data.empresa_id, data.cnpj)
        return JSONResponse(status_code=201, content={"id_filial": id_filial})
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.post("/Auth")
async def get_login(
    token: str = Header(...),
    service: InterfaceAuthService = Depends(get_controller_auth),
):
    try:
        service.auth(token)
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
    service: InterfaceFilialService = Depends(get_controller_filial),
    auth: InterfaceAuthService = Depends(get_controller_auth),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result = service.get_all()
        return JSONResponse(status_code=200, content=result)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/data/{day}")
async def get_data_day(
    token: str = Header(...),
    service: InterfaceFilialService = Depends(get_controller_filial),
):
    try:
        result = service.get_data_day(token)
        return JSONResponse(status_code=200, content=result)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
