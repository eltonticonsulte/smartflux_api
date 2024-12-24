# -*- coding: utf-8 -*-
from fastapi import APIRouter
from typing_extensions import Annotated, Doc
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from src.interfaces import InterfaceAuthController
from .core import auth2_admin, get_controller_auth

router = APIRouter()


@router.post("/login")
async def get_login(
    auth: Annotated[OAuth2PasswordRequestForm, Depends()],
    controller: InterfaceAuthController = Depends(get_controller_auth),
):
    try:
        print("####", auth.username, auth.password)
        token = controller.login(auth.username, auth.password)
        return JSONResponse(
            status_code=200,
            content={"access_token": token, "token_type": "bearer"},
        )
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/status")
async def get_status(
    token: str = Depends(auth2_admin),
    controller: InterfaceAuthController = Depends(get_controller_auth),
):
    nameuser = controller.current_user(token)
    return JSONResponse(status_code=200, content={"status": "ok", "name": nameuser})
