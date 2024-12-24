# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from ..composers import AuthComposer

router = APIRouter()


@router.post("/register")
async def get_login(token: Annotated[AuthComposer, Depends()]):
    return JSONResponse(
        status_code=200, content={"access_token": token, "token_type": "bearer"}
    )
