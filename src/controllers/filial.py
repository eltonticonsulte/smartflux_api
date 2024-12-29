# -*- coding: utf-8 -*-
from typing import List
from fastapi import APIRouter, Header
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.interfaces import InterfaceAuthService, InterfaceFilialService
from .core import auth2_admin, get_service_auth, get_service_filial
from ..dto import CreateFilialRequest, CreateFilialResponse, GetFilialResponse

router = APIRouter()


@router.post("/create", status_code=201, response_model=CreateFilialResponse)
async def create(
    request: CreateFilialRequest,
    token: str = Depends(auth2_admin),
    service: InterfaceFilialService = Depends(get_service_filial),
    auth: InterfaceAuthService = Depends(get_service_auth),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result: CreateFilialResponse = service.create(request)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.post("/Auth")
async def get_login(
    token: str = Header(...),
    service: InterfaceAuthService = Depends(get_service_auth),
):
    try:
        service.auth(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        return JSONResponse(
            status_code=200,
            content={"access_token": token, "token_type": "bearer"},
        )
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/all", status_code=200, response_model=List[GetFilialResponse])
async def get_all(
    token: str = Depends(auth2_admin),
    service: InterfaceFilialService = Depends(get_service_filial),
    auth: InterfaceAuthService = Depends(get_service_auth),
):
    try:
        auth.current_user(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    try:
        result: List[GetFilialResponse] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/data/{day}")
async def get_data_day(
    token: str = Header(...),
    service: InterfaceFilialService = Depends(get_service_filial),
):
    try:
        result = service.get_data_day(token)
        return JSONResponse(status_code=200, content=result)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
