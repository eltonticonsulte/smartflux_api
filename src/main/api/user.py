# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing_extensions import Annotated

from ..composers import AuthComposer, AuthComposerLogin
from .core import auth2_scheme

router = APIRouter()


@router.post("/login")
async def get_login(composer: Annotated[AuthComposerLogin, Depends()]):
    return JSONResponse(
        status_code=200,
        content={"access_token": composer.get_token(), "token_type": "bearer"},
    )


@router.get("/status")
async def get_status(
    auth: Annotated[AuthComposer, Depends()], token: str = Depends(auth2_scheme)
):
    nameuser = auth.current_user(token)
    return JSONResponse(status_code=200, content={"status": "ok", "name": nameuser})
