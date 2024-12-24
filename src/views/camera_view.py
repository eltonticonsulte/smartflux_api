# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceCameraController
from .core import auth2_admin, get_controller_camera

router = APIRouter()


class CreateCameraData(BaseModel):
    name: str
    zone_id: int


@router.post("/create")
async def create(
    camera: CreateCameraData,
    token: str = Depends(auth2_admin),
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
