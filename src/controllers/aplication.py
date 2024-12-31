# -*- coding: utf-8 -*-
import uuid
from fastapi import APIRouter, Header, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.interfaces import InterfaceUserService
from .core import get_service_user

router = APIRouter()


@router.post("/license", status_code=200, deprecated=True)
async def check_license(
    token: uuid.UUID = Header(...),
    service: InterfaceUserService = Depends(get_service_user),
):
    try:
        pass
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.post("/logs", status_code=200, deprecated=True)
async def get_logs(
    token: uuid.UUID = Header(...),
    service: InterfaceUserService = Depends(get_service_user),
):
    pass


@router.post("/status", status_code=200, deprecated=True)
async def post_status(
    token: uuid.UUID = Header(...),
    service: InterfaceUserService = Depends(get_service_user),
):
    nameuser = service.current_user(token)
    return JSONResponse(status_code=200, content={"status": "ok", "name": nameuser})
