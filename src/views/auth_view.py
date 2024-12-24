# -*- coding: utf-8 -*-
from fastapi import APIRouter
from typing_extensions import Annotated, Doc
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing_extensions import Annotated

from ..compose import FactoryController
from .core import auth2_admin

router = APIRouter()
controller = FactoryController().create_auth_controller()


@router.post("/login")
async def get_login(auth: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        token = controller.login(auth.username, auth.password)
        return JSONResponse(
            status_code=200,
            content={"access_token": token, "token_type": "bearer"},
        )
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/status")
async def get_status(token: str = Depends(auth2_admin)):
    nameuser = controller.curret_user(token)
    return JSONResponse(status_code=200, content={"status": "ok", "name": nameuser})
