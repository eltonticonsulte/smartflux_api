# -*- coding: utf-8 -*-
from fastapi import APIRouter, Header
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.interfaces import InterfaceAuthService, InterfaceZoneService
from .core import auth2_admin, get_service_auth, get_service_zone

router = APIRouter()


class ZonaData(BaseModel):
    name: str
    filial_id: int


@router.post("/create")
async def create(
    data: ZonaData = Depends(),
    token: str = Depends(auth2_admin),
    auth: InterfaceAuthService = Depends(get_service_auth),
    service: InterfaceZoneService = Depends(get_service_zone),
):
    try:
        pass
        # data = auth.curret_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))

    try:
        id_zone = service.create(data.name, data.filial_id)
        return JSONResponse(status_code=201, content={"id_zone": id_zone})
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/all")
async def get_all(
    token: str = Depends(auth2_admin),
    auth: InterfaceAuthService = Depends(get_service_auth),
    service: InterfaceZoneService = Depends(get_service_zone),
):
    try:
        auth.curret_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result = service.get_all()
        return JSONResponse(status_code=200, content=result)
    except Exception as error:
        raise HTTPException(500, detail=str(error))