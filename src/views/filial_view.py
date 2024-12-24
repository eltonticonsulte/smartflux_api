# -*- coding: utf-8 -*-
from fastapi import APIRouter, Header
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from pydantic import BaseModel
from .core import auth2_admin
from ..compose import FactoryController

router = APIRouter()
controller = FactoryController().create_filial_controller()
auth = FactoryController().create_auth_controller()


class CreateFilialData(BaseModel):
    name_filial: str
    empresa_id: int
    cnpj: str


@router.post("/create")
async def create(data: CreateFilialData, token: str = Depends(auth2_admin)):
    try:
        auth.curret_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        id_filial = controller.create(data.name_filial, data.empresa_id, data.cnpj)
        return JSONResponse(status_code=201, content={"id_filial": id_filial})
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.post("/Auth")
async def get_login(token: str = Header(...)):
    try:
        controller.auth(auth.username, auth.password)
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
async def get_all(token: str = Depends(auth2_admin)):
    try:
        auth.curret_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result = controller.get_all()
        return JSONResponse(status_code=200, content=result)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
