# -*- coding: utf-8 -*-
from fastapi import APIRouter, Header
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceAuthController, InterfaceZoneController
from .core import auth2_admin, get_controller_auth, get_controller_zone

router = APIRouter()


class FilialData(BaseModel):
    name: str
    filial_id: int


@router.post("/create")
async def create(
    token: str = Depends(auth2_admin),
    auth: InterfaceAuthController = Depends(get_controller_auth),
    controller: InterfaceZoneController = Depends(get_controller_zone),
):
    try:
        data = auth.curret_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))

    try:
        id_zone = controller.create(data.name, data.id_filial)
        return JSONResponse(status_code=201, content={"id_zone": id_zone})
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/all")
async def get_all(
    token: str = Depends(auth2_admin),
    auth: InterfaceAuthController = Depends(get_controller_auth),
    controller: InterfaceZoneController = Depends(get_controller_zone),
):
    try:
        auth.curret_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result = controller.get_all()
        return JSONResponse(status_code=200, content=result)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
