# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from .core import auth2_scheme
from ..composers import CreateFilialComposer

router = APIRouter()


@router.post("/create")
async def create(
    data: Annotated[CreateFilialComposer, Depends()], token: str = Depends(auth2_scheme)
):
    return JSONResponse(
        status_code=200,
        content={"access_token": data.get_token(), "token_type": "bearer"},
    )


@router.post("/login")
async def get_login(token: Annotated[CreateFilialComposer, Depends()]):
    pass


@router.get("/all")
async def get_all(token: str = Depends(auth2_scheme)):
    pass
