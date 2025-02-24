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
    RequestCreateCamera,
    ResponseCamera,
    RequestUpdateCamera,
    ResponseAuthUser,
    RequestStatus,
    UserPermissionAccessDTO,
)
from src.enums import UserRule
from .core import (
    get_service_camera,
    rule_require,
    get_service_filial,
    verificar_api_key,
)


router = APIRouter()
log = logging.getLogger("controller_camera")


@router.post("/create", status_code=201, response_model=ResponseCamera)
async def create(
    request: RequestCreateCamera,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceCameraService = Depends(get_service_camera),
):

    try:
        result: ResponseCamera = service.create(request)
        return result
    except ServiceUserJwtExecption as error:
        log.error("error", exc_info=error)
        raise HTTPException(401, detail=str(error))
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.post("/status", status_code=200)
async def status(
    data: RequestStatus,
    data_filial: ResponseAuthUser = Depends(verificar_api_key),
    service_camera: InterfaceCameraService = Depends(get_service_camera),
):

    try:
        service_camera.update_status(data)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/all", status_code=200, response_model=List[ResponseCamera])
async def get_all(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    service: InterfaceCameraService = Depends(get_service_camera),
):
    try:
        result: List[ResponseCamera] = service.get_all()
        return result
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.put("/update/{channel_id}", status_code=200, response_model=ResponseCamera)
async def update(
    channel_id: uuid.UUID,
    request: RequestUpdateCamera,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceCameraService = Depends(get_service_camera),
):

    try:
        result: ResponseCamera = service.update(channel_id, request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.delete("/delete/{channel_id}", status_code=200)
async def delete(
    channel_id: uuid.UUID,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceCameraService = Depends(get_service_camera),
):

    try:
        service.delete(channel_id)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/list-name-device", status_code=200, response_model=List[str])
async def get_lista_name_camera(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    service: InterfaceCameraService = Depends(get_service_camera),
) -> List[str]:
    try:
        if user.filial_id:
            result: List[str] = service.get_list_name_camera_by_filial(user.filial_id)
            return result

    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/list-zone", status_code=200, response_model=List[str])
async def get_lista_tag_camera(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    service: InterfaceCameraService = Depends(get_service_camera),
) -> List[str]:
    try:
        if user.filial_id:
            result: List[str] = service.get_list_tag_by_filial(user.filial_id)
            return result
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))
