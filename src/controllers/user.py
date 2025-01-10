# -*- coding: utf-8 -*-
from logging import getLogger
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.interfaces import InterfaceUserService
from src.dto import (
    AuthUserResponse,
    AuthUserRequest,
    CreateUserRequest,
    GetUserResponse,
)
from src.enums import UserRole
from .core import auth2_admin, get_service_user


router = APIRouter()
log = getLogger("controller user")


@router.post("/login", response_model=AuthUserResponse, status_code=200)
async def get_login(
    auth: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: InterfaceUserService = Depends(get_service_user),
):
    try:
        result: AuthUserResponse = service.auth_user(
            AuthUserRequest(username=auth.username, password=auth.password)
        )
        return result
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.post("/create", status_code=200)
async def create(
    request: CreateUserRequest,
    token: str = Depends(auth2_admin),
    service: InterfaceUserService = Depends(get_service_user),
):
    try:
        user: GetUserResponse = service.current_user(token)
        if not user.is_admin():
            raise HTTPException(401, detail="Unauthorized")
        print(request.role, type(request.role))
        result: AuthUserResponse = service.create(request)
        return result
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/status", status_code=200, response_model=GetUserResponse)
async def get_status(
    token: str = Depends(auth2_admin),
    service: InterfaceUserService = Depends(get_service_user),
):
    try:
        user = service.current_user(token)
        return user
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))
