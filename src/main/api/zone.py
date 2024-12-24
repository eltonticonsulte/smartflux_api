# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from .core import auth2_scheme
from ..composers import CreateZoneCompose, GetZoneCompose

router = APIRouter()
LOG = logging.getLogger(__name__)


@router.post("/create")
async def create(
    data: Annotated[CreateZoneCompose, Depends()], token: str = Depends(auth2_scheme)
):
    return JSONResponse(
        status_code=200,
        content={"access_token": data.get_token(), "token_type": "bearer"},
    )


@router.get("/all")
async def get_all(
    controller: Annotated[GetZoneCompose, Depends()], token: str = Depends(auth2_scheme)
):
    try:
        return JSONResponse(status_code=200, content=controller.get_all())
    except Exception as error:
        LOG.error(error, exc_info=error)
        return HTTPException(500, detail=str(error))
