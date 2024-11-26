# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter, status, HTTPException, File

from model.event import EventReciver

router_event_counter = APIRouter()
logger = logging.getLogger(__name__)


@router_event_counter.post("/event-count", status_code=status.HTTP_200_OK)
async def post_auto_update(data: EventReciver) -> str:
    logger.info(data)
    return f"ok"
