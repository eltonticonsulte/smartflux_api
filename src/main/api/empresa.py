# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from ..composers import AuthComposer

router = APIRouter()


@router.post("/create")
async def create(from_data: OAuth2PasswordRequestForm = Depends()):
    pass


@router.get("/all")
async def get_all():
    pass
