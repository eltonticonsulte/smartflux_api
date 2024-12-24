# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing_extensions import Annotated

from ..composers import AuthComposer, AuthComposerLogin
from .core import auth2_scheme

router = APIRouter()


@router.post("/login")
async def get_login(composer: Annotated[AuthComposerLogin, Depends()]):

    try:
        token = composer.get_token()
        return JSONResponse(
            status_code=200,
            content={"access_token": token, "token_type": "bearer"},
        )
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/status")
async def get_status(
    auth: Annotated[AuthComposer, Depends()], token: str = Depends(auth2_scheme)
):
    nameuser = auth.current_user(token)
    return JSONResponse(status_code=200, content={"status": "ok", "name": nameuser})
