# -*- coding: utf-8 -*-
from fastapi import APIRouter
from typing_extensions import Annotated, Doc
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from src.interfaces import InterfaceAuthService
from .core import auth2_admin, get_service_auth

router = APIRouter()


@router.post("/login")
async def get_login(
    auth: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: InterfaceAuthService = Depends(get_service_auth),
):
    try:
        token = service.auth_user(auth.username, auth.password)
        return JSONResponse(
            status_code=200,
            content={"access_token": token, "token_type": "bearer"},
        )
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/status")
async def get_status(
    token: str = Depends(auth2_admin),
    service: InterfaceAuthService = Depends(get_service_auth),
):
    nameuser = service.current_user(token)
    return JSONResponse(status_code=200, content={"status": "ok", "name": nameuser})
