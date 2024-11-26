# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter, status, HTTPException, File


router_client = APIRouter()
logger = logging.getLogger(__name__)


@router_client.post("/create_camera", status_code=status.HTTP_200_OK)
async def create(data) -> str:
    return f"ok"


@router_client.put("/update", status_code=status.HTTP_200_OK)
async def update(data) -> str:
    return f"ok"


@router_client.delete("/delete", status_code=status.HTTP_200_OK)
async def delete(data) -> str:
    return f"ok"
