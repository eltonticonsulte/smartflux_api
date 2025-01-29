# -*- coding: utf-8 -*-
from logging import getLogger
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header
from src.enums import UserRule
from src.interfaces import InterfaceEventService, InterfaceFilialService
from src.services import WebSocketNotifierService

from src.dto import (
    RequestEventCount,
    ResponseEventCount,
    UserPermissionAccessDTO,
    EventCountDataValidate,
)
from ..core import (
    get_service_count_event,
    rule_require,
    get_service_websocket,
    get_service_filial,
)

router = APIRouter()
log = getLogger("controller_count_event")


@router.post("/count", status_code=200, response_model=ResponseEventCount)
async def create_event(
    request: RequestEventCount,
    token: UUID = Header(...),
    filial_service: InterfaceFilialService = Depends(get_service_filial),
    event_service: InterfaceEventService = Depends(get_service_count_event),
):
    log.info(f"create_event {request}")
    try:
        filial_service.check_token(token)
    except Exception as error:
        log.error(f"error: request {request}", exc_info=error)
        raise HTTPException(401, detail=str(error))
    try:
        result: ResponseEventCount = event_service.create_event(request)
        return result
    except Exception as error:
        log.error(f"error: request {request}", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.post("/counts", status_code=201, response_model=List[EventCountDataValidate])
async def insert_event(
    request: List[RequestEventCount],
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceEventService = Depends(get_service_count_event),
) -> List[EventCountDataValidate]:
    if user.rule != UserRule.FILIAL:
        raise HTTPException(
            401, detail=f"Apenas Filiar pode registrar eventos vc é {user.rule}"
        )
    if user.filial_id is None:

        raise HTTPException(401, detail="O usuário não possui filial")
    try:
        log.info(f"insert_event {request}")
        result: List[EventCountDataValidate] = await count_event.process_events(
            request, user
        )
        return result
    except Exception as error:
        log.error(f"error: request {request}", exc_info=error)
        raise HTTPException(500, detail=str(error))
