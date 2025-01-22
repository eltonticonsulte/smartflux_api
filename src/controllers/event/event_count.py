# -*- coding: utf-8 -*-
from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.enums import UserRule
from src.interfaces import InterfaceEventService
from src.services import WebSocketNotifierService

from src.dto import (
    EventCountRequest,
    EventCountResponse,
    UserPermissionAccessDTO,
    EventCountDataValidate,
)
from ..core import get_service_count_event, rule_require, get_service_websocket

router = APIRouter()
log = getLogger("controller_count_event")


@router.post("/count", status_code=201, response_model=List[EventCountDataValidate])
async def insert_event(
    request: List[EventCountRequest],
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceEventService = Depends(get_service_count_event),
    websocket: WebSocketNotifierService = Depends(get_service_websocket),
) -> List[EventCountDataValidate]:
    if user.rule != UserRule.FILIAL:
        raise HTTPException(
            401, detail=f"Apenas Filiar pode registrar eventos vc é {user.rule}"
        )
    if user.filial_id is None:

        raise HTTPException(401, detail="O usuário não possui filial")
    try:
        log.info(f"insert_event {request}")
        result: List[EventCountDataValidate] = await count_event.process_event(
            request, user
        )

        await websocket.process_websocket(result, user.filial_id)
        return result
    except Exception as error:
        log.error(f"error: request {request}", exc_info=error)
        raise HTTPException(500, detail=str(error))
