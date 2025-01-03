# -*- coding: utf-8 -*-
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.interfaces import InterfaceCameraService, InterfaceUserService
from src.dto import (
    CreateCameraRequest,
    GetCameraResponse,
    UpdateCameraRequest,
)
from .core import auth2_admin, get_service_camera, get_service_user

router = APIRouter()


@router.post("/create", status_code=201, response_model=GetCameraResponse)
async def create(
    request: CreateCameraRequest,
    token: uuid.UUID = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceCameraService = Depends(get_service_camera),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result: GetCameraResponse = service.create(request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/status")
async def get_status(
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceCameraService = Depends(get_service_camera),
):
    try:
        service.current_user(get_service_user)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    return JSONResponse(status_code=200, content={"status": "ok", "name": "nameuser"})


@router.get("/all", status_code=200, response_model=List[GetCameraResponse])
async def get_all(
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceCameraService = Depends(get_service_camera),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result: List[GetCameraResponse] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.put("/update/{channel_id}", status_code=200, response_model=GetCameraResponse)
async def update(
    channel_id: uuid.UUID,
    request: UpdateCameraRequest,
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceCameraService = Depends(get_service_camera),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result: GetCameraResponse = service.update(channel_id, request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.delete("/delete/{channel_id}", status_code=200)
async def delete(
    channel_id: uuid.UUID,
    token: str = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    service: InterfaceCameraService = Depends(get_service_camera),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))

    try:
        service.delete(channel_id)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))
