# -*- coding: utf-8 -*-
from fastapi import APIRouter, Header
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from ..compose import FactoryController

router = APIRouter()
controller = FactoryController().create_counter_event_controller()


@router.post("/register")
async def get_login(token: str = Header(...)):
    try:
        controller.register(token)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
