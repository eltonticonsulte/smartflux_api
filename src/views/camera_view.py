# -*- coding: utf-8 -*-
import uuid
from fastapi import APIRouter, Header
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceCameraController
from .core import auth2_admin, get_controller_camera
from src.dto import CountEventDTO

router = APIRouter()


class CreateCameraData(BaseModel):
    name: str
    zone_id: int


from pydantic import BaseModel
from typing import List


class CountEventData(BaseModel):
    events: List[CountEventDTO]


@router.post("/create")
async def create(
    camera: CreateCameraData,
    token: uuid.UUID = Depends(auth2_admin),
    controller: InterfaceCameraController = Depends(get_controller_camera),
):
    try:
        controller.create(camera.name, camera.zone_id)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/status")
async def get_status(
    token: str = Depends(auth2_admin),
    controller: InterfaceCameraController = Depends(get_controller_camera),
):
    controller.current_user()
    return JSONResponse(status_code=200, content={"status": "ok", "name": "nameuser"})


@router.get("/all")
async def get_all(
    token: str = Depends(auth2_admin),
    controller: InterfaceCameraController = Depends(get_controller_camera),
):
    try:
        result = controller.get_all()
        return JSONResponse(status_code=200, content=result)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.post("/event")
async def insert_event(
    data: CountEventData = Depends(),
    token: uuid.UUID = Header(...),
    controller: InterfaceCameraController = Depends(get_controller_camera),
):
    try:
        controller.validate_token(token)
        result = controller.register_event(data.events)
        return JSONResponse(status_code=200, content=result)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
