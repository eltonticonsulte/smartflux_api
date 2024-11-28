# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter, status, HTTPException, File

from src.entity.visitorEntity import PullEventReciver

router_event_counter = APIRouter()
logger = logging.getLogger(__name__)


@router_event_counter.post("/event-count", status_code=status.HTTP_200_OK)
async def post_auto_update(data: PullEventReciver) -> str:
    try:
        logger.info(data)
    except Exception as error:
        return HTTPException(422, detail=error)

    return f"ok"
