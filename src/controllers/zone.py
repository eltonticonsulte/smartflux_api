# -*- coding: utf-8 -*-
from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, Depends
from src.interfaces import InterfaceZoneService
from src.enums import UserRule
from .core import get_service_zone, rule_require
from ..dto import (
    CreateZoneRequest,
    GetZoneResponse,
    UpdateZoneRequest,
    UserPermissionAccessDTO,
)

router = APIRouter()


@router.post("/create", status_code=201, response_model=GetZoneResponse)
async def create(
    request: CreateZoneRequest,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceZoneService = Depends(get_service_zone),
):
    try:
        result: GetZoneResponse = service.create(request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/all", status_code=200, response_model=List[GetZoneResponse])
async def get_all(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceZoneService = Depends(get_service_zone),
):

    try:
        result: List[GetZoneResponse] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.put("/update/{zona_id}", status_code=200, response_model=GetZoneResponse)
async def update(
    zona_id: int,
    request: UpdateZoneRequest,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceZoneService = Depends(get_service_zone),
):

    try:
        result: GetZoneResponse = service.update(zona_id, request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.delete("/delete/{zona_id}", status_code=200)
async def delete(
    zona_id: int,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceZoneService = Depends(get_service_zone),
):

    try:
        service.delete(zona_id)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))
