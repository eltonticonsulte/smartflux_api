# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceEmpresaController, InterfaceAuthController
from .core import auth2_admin, get_controller_auth, get_controller_empresa

router = APIRouter()


class EmpresaData(BaseModel):
    name: str


@router.post("/create", status_code=201)
async def create(
    empresa: EmpresaData,
    token: str = Depends(auth2_admin),
    controller: InterfaceEmpresaController = Depends(get_controller_empresa),
    controller_auth: InterfaceAuthController = Depends(get_controller_auth),
):
    user = controller_auth.curret_user(token)
    if not user:
        raise HTTPException(401, detail="Unauthorized")
    try:
        id_empresa = controller.create(empresa.name)
        return JSONResponse(status_code=201, content={"id_empresa": id_empresa})
    except Exception as error:
        raise HTTPException(422, detail=str(error))


@router.get("/all")
async def get_all(
    token: str = Depends(auth2_admin),
    controller: InterfaceEmpresaController = Depends(get_controller_empresa),
):
    try:
        get_controller_auth.curret_user(token)
    except Exception:
        raise HTTPException(401, detail="Unauthorized")
    result = controller.get_all()
    return JSONResponse(status_code=200, content=result)
