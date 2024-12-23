# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from ..composers import AuthComposer

router = APIRouter(prefix="/counter-event")


@router.post("/create")
async def create(data: Annotated[AuthComposer, Depends()]):
    return JSONResponse(
        status_code=200,
        content={"access_token": data.get_token(), "token_type": "bearer"},
    )


@router.post("/login")
async def get_login(token: Annotated[AuthComposer, Depends()]):
    pass


@router.get("/all")
async def get_all():
    pass
