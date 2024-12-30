# -*- coding: utf-8 -*-
from typing import List
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Depends
from src.interfaces import InterfaceUserService, InterfaceZoneService
from .core import auth2_admin, get_service_user, get_service_zone
from ..dto import (
    CreateZoneRequest,
    CreateZoneResponse,
    GetZoneResponse,
    UpdateZoneRequest,
)

router = APIRouter()


@router.post("/create", status_code=201, response_model=CreateZoneResponse)
async def create(
    request: CreateZoneRequest,
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceZoneService = Depends(get_service_zone),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))

    try:
        result: CreateZoneResponse = service.create(request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/all", status_code=200, response_model=List[GetZoneResponse])
async def get_all(
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceZoneService = Depends(get_service_zone),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result: List[GetZoneResponse] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.put("/update/{id}", status_code=200, response_model=GetZoneResponse)
async def update(
    id: int,
    request: UpdateZoneRequest,
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceZoneService = Depends(get_service_zone),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result: GetZoneResponse = service.update(id, request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.delete("/delete/{id}", status_code=200)
async def delete(
    id: int,
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceZoneService = Depends(get_service_zone),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        service.delete(id)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))
