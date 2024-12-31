# -*- coding: utf-8 -*-
from typing import List
from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.interfaces import InterfaceUserService, InterfaceFilialService
from .core import auth2_admin, get_service_user, get_service_filial
from ..dto import (
    CreateFilialRequest,
    GetFilialResponse,
    UpdateFilialRequest,
)

router = APIRouter()


@router.post("/create", status_code=201, response_model=GetFilialResponse)
async def create(
    request: CreateFilialRequest,
    token: str = Depends(auth2_admin),
    service: InterfaceFilialService = Depends(get_service_filial),
    auth: InterfaceUserService = Depends(get_service_user),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result: GetFilialResponse = service.create(request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.post("/auth", status_code=200, response_model=GetFilialResponse)
async def get_login(
    name_filial: str = Header(...),
    token: str = Header(...),
    service: InterfaceFilialService = Depends(get_service_filial),
):
    current_filial = None
    try:
        current_filial = service.get_by_token(token)
        if current_filial.name != name_filial:
            raise Exception("Nome de filial inválido")
        return current_filial
    except Exception as error:
        raise HTTPException(401, detail=str(error))


@router.get("/all", status_code=200, response_model=List[GetFilialResponse])
async def get_all(
    token: str = Depends(auth2_admin),
    service: InterfaceFilialService = Depends(get_service_filial),
    auth: InterfaceUserService = Depends(get_service_user),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result: List[GetFilialResponse] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.put("/update/{filial_id}", status_code=200, response_model=GetFilialResponse)
async def update(
    filial_id: int,
    request: UpdateFilialRequest,
    token: str = Depends(auth2_admin),
    service: InterfaceFilialService = Depends(get_service_filial),
    auth: InterfaceUserService = Depends(get_service_user),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result: GetFilialResponse = service.update(filial_id, request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.delete("/delete/{filial_id}", status_code=200)
async def delete(
    filial_id: int,
    token: str = Depends(auth2_admin),
    service: InterfaceFilialService = Depends(get_service_filial),
    auth: InterfaceUserService = Depends(get_service_user),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        service.delete(filial_id)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))
