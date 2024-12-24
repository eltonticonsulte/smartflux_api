# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceCameraController
from ..compose import FactoryController
from .core import auth2_admin

router = APIRouter()


def controller_camera() -> InterfaceCameraController:
    return FactoryController().create_camera_controller()


class CreateCameraData(BaseModel):
    name: str
    zone_id: int


@router.post("/create")
async def create(
    camera: CreateCameraData,
    token: str = Depends(auth2_admin),
    controller: InterfaceCameraController = Depends(controller_camera),
):
    try:
        controller.create(camera.name, camera.zone_id)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/status")
async def get_status(
    token: str = Depends(auth2_admin),
    controller: InterfaceCameraController = Depends(controller_camera),
):
    controller.get_all()
    return JSONResponse(status_code=200, content={"status": "ok", "name": nameuser})


@router.get("/all")
async def get_all(
    token: str = Depends(auth2_admin),
    controller: InterfaceCameraController = Depends(controller_camera),
):
    try:
        result = controller.get_all()
        return JSONResponse(status_code=200, content=result)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
