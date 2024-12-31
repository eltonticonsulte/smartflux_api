# -*- coding: utf-8 -*-
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.interfaces import InterfaceEmpresaService, InterfaceUserService
from .core import auth2_admin, get_service_user, get_service_empresa
from ..dto import (
    CreateEmpresaRequest,
    GetEmpresaResponse,
    UpdateEmpresaRequest,
)

router = APIRouter()


@router.post("/create", status_code=201, response_model=GetEmpresaResponse)
async def create(
    request: CreateEmpresaRequest,
    token: str = Depends(auth2_admin),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
    auth: InterfaceUserService = Depends(get_service_user),
):
    user = auth.current_user(token)
    if not user:
        raise HTTPException(401, detail="Unauthorized")
    try:
        result: GetEmpresaResponse = service.create(request)
        return result
    except Exception as error:
        raise HTTPException(422, detail=str(error))


@router.get("/all", status_code=200, response_model=List[GetEmpresaResponse])
async def get_all(
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(
            401, detail=f"Unauthorized: {error}", headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        result: List[GetEmpresaResponse] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/get/{empresa_id}", status_code=200, response_model=GetEmpresaResponse)
async def get_by_id(
    empresa_id: int,
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
):
    try:
        auth.current_user(token)
    except Exception:
        raise HTTPException(401, detail="Unauthorized")
    try:
        result: GetEmpresaResponse = service.get_by_id(empresa_id)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.put("/update/{empresa_id}", status_code=200, response_model=GetEmpresaResponse)
async def update(
    empresa_id: int,
    request: UpdateEmpresaRequest,
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(
            401, detail=f"Unauthorized: {error}", headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        result: GetEmpresaResponse = service.update(empresa_id, request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.delete("/delete/{empresa_id}", status_code=200)
async def delete(
    empresa_id: int,
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(
            401, detail=f"Unauthorized: {error}", headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        service.delete(empresa_id)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))
