# -*- coding: utf-8 -*-
from logging import getLogger
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.interfaces import InterfaceFilialService
from src.enums import UserRule
from .core import get_service_filial, rule_require
from ..dto import (
    RequestCreateFilial,
    ResponseFilial,
    RequestUpdateFilial,
    UserPermissionAccessDTO,
)

router = APIRouter()
log = getLogger("controller Filial")


@router.post("/create", status_code=201, response_model=ResponseFilial)
async def create(
    request: RequestCreateFilial,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceFilialService = Depends(get_service_filial),
):
    try:
        result: ResponseFilial = service.create(request)
        return result
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/me", status_code=200, response_model=ResponseFilial)
async def get_me(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    service: InterfaceFilialService = Depends(get_service_filial),
) -> ResponseFilial:
    try:
        if not user.filial_id:
            raise HTTPException(400, detail="User not filial perimssion")
        return service.get_by_id(user.filial_id)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/all", status_code=200, response_model=List[ResponseFilial])
async def get_all(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.EMPRESA)),
    service: InterfaceFilialService = Depends(get_service_filial),
):
    try:
        result: List[ResponseFilial] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.put("/update/{filial_id}", status_code=200, response_model=ResponseFilial)
async def update(
    filial_id: int,
    request: RequestUpdateFilial,
    service: InterfaceFilialService = Depends(get_service_filial),
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.EMPRESA)),
):
    try:
        result: ResponseFilial = service.update(filial_id, request)
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
