# -*- coding: utf-8 -*-
from fastapi import APIRouter
from typing_extensions import Annotated, Doc
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from src.interfaces import InterfaceUserService
from .core import auth2_admin, get_service_user
from src.dto import AuthUserResponse, CreateUserRequest, AuthUserRequest

router = APIRouter()


@router.post("/login", response_model=AuthUserResponse, status_code=200)
async def get_login(
    auth: Annotated[AuthUserRequest, Depends()],
    service: InterfaceUserService = Depends(get_service_user),
):
    try:
        result: AuthUserResponse = service.auth_user(auth.username, auth.password)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/status", status_code=200)
async def get_status(
    token: str = Depends(auth2_admin),
    service: InterfaceUserService = Depends(get_service_user),
):
    nameuser = service.current_user(token)
    return JSONResponse(status_code=200, content={"status": "ok", "name": nameuser})
