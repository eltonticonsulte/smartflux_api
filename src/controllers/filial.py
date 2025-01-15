# -*- coding: utf-8 -*-
from logging import getLogger
from typing import List
from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.interfaces import InterfaceUserService, InterfaceFilialService
from src.enums import UserRule
from .core import auth2_admin, get_service_user, get_service_filial, rule_require
from ..dto import (
    CreateFilialRequest,
    GetFilialResponse,
    UpdateFilialRequest,
    UserPermissionAccessDTO,
)

router = APIRouter()
log = getLogger("controller Filial")


@router.post("/create", status_code=201, response_model=GetFilialResponse)
async def create(
    request: CreateFilialRequest,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceFilialService = Depends(get_service_filial),
):
    try:
        result: GetFilialResponse = service.create(request)
        return result
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/all", status_code=200, response_model=List[GetFilialResponse])
async def get_all(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.EMPRESA)),
    service: InterfaceFilialService = Depends(get_service_filial),
):
    try:
        result: List[GetFilialResponse] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.put("/update/{filial_id}", status_code=200, response_model=GetFilialResponse)
async def update(
    filial_id: int,
    request: UpdateFilialRequest,
    service: InterfaceFilialService = Depends(get_service_filial),
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.EMPRESA)),
):
    try:
        result: GetFilialResponse = service.update(filial_id, request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.delete("/delete/{filial_id}", status_code=200)
async def delete(
    filial_id: int,
    service: InterfaceFilialService = Depends(get_service_filial),
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.EMPRESA)),
):
    try:
        service.delete(filial_id)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))
