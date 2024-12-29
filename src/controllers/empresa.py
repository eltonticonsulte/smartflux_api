# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceEmpresaService, InterfaceAuthService
from .core import auth2_admin, get_service_auth, get_service_empresa

router = APIRouter()


class EmpresaData(BaseModel):
    name: str


@router.post("/create", status_code=201)
async def create(
    empresa: EmpresaData,
    token: str = Depends(auth2_admin),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
    auth: InterfaceAuthService = Depends(get_service_auth),
):
    user = auth.current_user(token)
    if not user:
        raise HTTPException(401, detail="Unauthorized")
    try:
        id_empresa = service.create(empresa.name)
        return JSONResponse(status_code=201, content={"id_empresa": id_empresa})
    except Exception as error:
        raise HTTPException(422, detail=str(error))


@router.get("/all")
async def get_all(
    token: str = Depends(auth2_admin),
    auth: InterfaceAuthService = Depends(get_service_auth),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
):
    try:
        auth.current_user(token)
    except Exception:
        raise HTTPException(401, detail="Unauthorized")
    result = service.get_all()
    return JSONResponse(status_code=200, content=result)
