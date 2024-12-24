# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from pydantic import BaseModel
from .core import auth2_admin
from ..compose import FactoryController

router = APIRouter()
LOG = logging.getLogger(__name__)
controller = FactoryController().create_zone_controller()
auth = FactoryController().create_auth_controller()


class FilialData(BaseModel):
    name: str
    filial_id: int


@router.post("/create")
async def create(token: str = Depends(auth2_admin)):
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
async def get_all(token: str = Depends(auth2_admin)):
    try:
        auth.curret_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result = controller.get_all()
        return JSONResponse(status_code=200, content=result)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
