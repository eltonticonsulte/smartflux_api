# -*- coding: utf-8 -*-
import uuid
from fastapi import APIRouter, Header
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceCameraService
from .core import auth2_admin, get_service_camera
from src.dto import (
    EventCountRequest,
    EventCountResponse,
    CreateCameraRequest,
    CreateCameraResponse,
    GetCameraResponse,
)

router = APIRouter()

from typing import List


@router.post("/create", status_code=201, response_model=CreateCameraResponse)
async def create(
    request: CreateCameraRequest,
    token: uuid.UUID = Depends(auth2_admin),
    service: InterfaceCameraService = Depends(get_service_camera),
):
    try:
        result: CreateCameraResponse = service.create(request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/status")
async def get_status(
    token: str = Depends(auth2_admin),
    service: InterfaceCameraService = Depends(get_service_camera),
):
    service.current_user()
    return JSONResponse(status_code=200, content={"status": "ok", "name": "nameuser"})


@router.get("/all", status_code=200, response_model=List[GetCameraResponse])
async def get_all(
    token: str = Depends(auth2_admin),
    service: InterfaceCameraService = Depends(get_service_camera),
):
    try:
        result: List[GetCameraResponse] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))
