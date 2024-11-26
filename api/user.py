# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter, status, HTTPException, UploadFile, File


router_user = APIRouter()
logger = logging.getLogger(__name__)


@router_user.post("/login", status_code=status.HTTP_200_OK)
async def post_auto_update(data) -> str:
    return f"ok"
