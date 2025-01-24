# -*- coding: utf-8 -*-
import uuid
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from src.interfaces import (
    InterfaceCameraService,
    InterfaceUserService,
    InterfaceFilialService,
)
from src.exceptions import ServiceUserJwtExecption
from src.dto import (
    CreateCameraRequest,
    GetCameraResponse,
    UpdateCameraRequest,
    AuthUserResponse,
)
from src.enums import UserRule
from .core import get_service_camera, rule_require, get_service_filial


router = APIRouter()
log = logging.getLogger("controller_camera")


@router.post("/create", status_code=201, response_model=GetCameraResponse)
async def create(
    request: CreateCameraRequest,
    user: AuthUserResponse = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceCameraService = Depends(get_service_camera),
):

    try:
        result: GetCameraResponse = service.create(request)
        return result
    except ServiceUserJwtExecption as error:
        log.error("error", exc_info=error)
        raise HTTPException(401, detail=str(error))
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.post("/ping", status_code=200)
async def ping(
    token_filial: uuid.UUID = Header(...),
    token_camera: uuid.UUID = Header(...),
    service_filial: InterfaceFilialService = Depends(get_service_filial),
    service_camera: InterfaceCameraService = Depends(get_service_camera),
):
    try:
        service_filial.check_token(token_filial)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(401, detail=str(error))

    try:
        service_camera.ping(token_camera)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/all", status_code=200, response_model=List[GetCameraResponse])
async def get_all(
    user: AuthUserResponse = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceCameraService = Depends(get_service_camera),
):

    try:
        result: List[GetCameraResponse] = service.get_all()
        return result
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.put("/update/{channel_id}", status_code=200, response_model=GetCameraResponse)
async def update(
    channel_id: uuid.UUID,
    request: UpdateCameraRequest,
    user: AuthUserResponse = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceCameraService = Depends(get_service_camera),
):

    try:
        result: GetCameraResponse = service.update(channel_id, request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.delete("/delete/{channel_id}", status_code=200)
async def delete(
    channel_id: uuid.UUID,
    user: AuthUserResponse = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceCameraService = Depends(get_service_camera),
):

    try:
        service.delete(channel_id)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))
