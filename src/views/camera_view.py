# -*- coding: utf-8 -*-
import uuid
from fastapi import APIRouter, Header
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceCameraController
from .core import auth2_admin, get_controller_camera

router = APIRouter()


class CreateCameraData(BaseModel):
    name: str
    zone_id: int


from pydantic import BaseModel
from typing import List, Optional


class CountEventData(BaseModel):
    event_id: Optional[int]
    channel_id: str
    event_time: str
    count_in: int
    count_out: int
    camera_id: Optional[int]

    def to_dict(self):
        return self.model_dump()


class PullCountEventData(BaseModel):
    events: List[CountEventData]


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
    data: PullCountEventData,
    token: uuid.UUID = Header(...),
    controller: InterfaceCameraController = Depends(get_controller_camera),
):
    try:
        controller.validate_token(token)
        controller.register_event(data)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))
