# -*- coding: utf-8 -*-
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.interfaces import InterfaceEmpresaService, InterfaceUserService
from src.enums import UserRole
from .core import auth2_admin, get_service_user, get_service_empresa, rule_require
from ..dto import (
    CreateEmpresaRequest,
    GetEmpresaResponse,
    UpdateEmpresaRequest,
    AuthUserResponse,
)

router = APIRouter()


@router.post("/create", status_code=201, response_model=GetEmpresaResponse)
async def create(
    request: CreateEmpresaRequest,
    service: InterfaceEmpresaService = Depends(get_service_empresa),
    user: AuthUserResponse = Depends(rule_require(UserRole.ADMIN)),
):
    try:
        result: GetEmpresaResponse = service.create(request)
        return result
    except Exception as error:
        raise HTTPException(422, detail=str(error))


@router.get("/all", status_code=200, response_model=List[GetEmpresaResponse])
async def get_all(
    user: AuthUserResponse = Depends(rule_require(UserRole.ADMIN)),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
):

    try:
        result: List[GetEmpresaResponse] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/get/{empresa_id}", status_code=200, response_model=GetEmpresaResponse)
async def get_by_id(
    empresa_id: int,
    user: AuthUserResponse = Depends(rule_require(UserRole.ADMIN)),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
):
    try:
        result: GetEmpresaResponse = service.get_by_id(empresa_id)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.put("/update/{empresa_id}", status_code=200, response_model=GetEmpresaResponse)
async def update(
    empresa_id: int,
    request: UpdateEmpresaRequest,
    user: AuthUserResponse = Depends(rule_require(UserRole.ADMIN)),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
):

    try:
        result: GetEmpresaResponse = service.update(empresa_id, request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.delete("/delete/{empresa_id}", status_code=200)
async def delete(
    empresa_id: int,
    user: AuthUserResponse = Depends(rule_require(UserRole.ADMIN)),
    service: InterfaceEmpresaService = Depends(get_service_empresa),
):
    try:
        service.delete(empresa_id)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))
