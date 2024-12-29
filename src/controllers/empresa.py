# -*- coding: utf-8 -*-
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceEmpresaService, InterfaceAuthService
from .core import auth2_admin, get_service_auth, get_service_empresa
from ..dto import CreateRequestEmpresa, CreateResponseEmpresa, GetResponseEmpresa

router = APIRouter()


@router.post("/create", status_code=201, response_model=CreateResponseEmpresa)
async def create(
    request: CreateRequestEmpresa,
    token: str = Depends(auth2_admin),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
    auth: InterfaceAuthService = Depends(get_service_auth),
):
    user = auth.current_user(token)
    if not user:
        raise HTTPException(401, detail="Unauthorized")
    try:
        result: CreateResponseEmpresa = service.create(request)
        return result
    except Exception as error:
        raise HTTPException(422, detail=str(error))


@router.get("/all", status_code=200, response_model=List[GetResponseEmpresa])
async def get_all(
    token: str = Depends(auth2_admin),
    auth: InterfaceAuthService = Depends(get_service_auth),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
):
    try:
        auth.current_user(token)
    except Exception:
        raise HTTPException(401, detail="Unauthorized")
    try:
        result: List[GetResponseEmpresa] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))
