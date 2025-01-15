# -*- coding: utf-8 -*-
from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi import WebSocket, WebSocketDisconnect
from src.enums import UserRule
from src.interfaces import (
    InterfaceTodayStorageService,
    InterfaceEventService,
    InterfaceUserService,
)
from src.observers import DataEventWebSocketNotifier
from src.dto import (
    EventCountRequest,
    EventCountResponse,
    TotalCount,
    TotalCountGrupZone,
    TotalCountGrupHour,
    UserPermissionAccessDTO,
)
from .core import (
    get_service_count_event,
    rule_require,
    get_service_user,
    get_current_event_websocket,
)

router = APIRouter()
log = getLogger("controller_count_event")


@router.post("/count", status_code=201, response_model=List[EventCountResponse])
async def insert_event(
    request: List[EventCountRequest],
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceEventService = Depends(get_service_count_event),
) -> List[EventCountResponse]:
    if user.rule != UserRule.FILIAL:
        raise HTTPException(
            401, detail=f"Apenas Filiar pode registrar eventos vc é {user.rule}"
        )
    if user.filial_id is None:

        raise HTTPException(401, detail="O usuário não possui filial")
    try:
        log.info(f"insert_event {request}")
        result: List[EventCountResponse] = await count_event.process_event(
            request, user
        )
        return result
    except Exception as error:
        log.error(f"error: request {request}", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/total/current-today", status_code=200, response_model=TotalCount)
async def get_data_day(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceTodayStorageService = Depends(get_service_count_event),
) -> TotalCount:

    try:
        return count_event.get_count_by_filial(user.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get(
    "/total/grup-zone", status_code=200, response_model=List[TotalCountGrupZone]
)
async def get_data_filial_grup_zone(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceTodayStorageService = Depends(get_service_count_event),
) -> List[TotalCountGrupZone]:
    try:
        return count_event.get_count_by_filial_count_grup_zone(user.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get(
    "/total/grup-hour", status_code=200, response_model=List[TotalCountGrupHour]
)
async def get_data_filial_grup_hour(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceTodayStorageService = Depends(get_service_count_event),
) -> List[TotalCountGrupHour]:
    try:
        return count_event.get_count_by_filial_grup_hour(user.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):
    headers = websocket.headers
    log.debug(headers)
    authorization = headers.get("Authorization")

    if authorization is None:
        websocket.close(code=400, reason="Token de autorização ausente")
        return

    token = authorization.split(" ")[1]
    service: InterfaceUserService = get_service_user()
    user: UserPermissionAccessDTO = service.current_user(token)

    log.debug(user)
    if not user.is_active:
        websocket.close(code=400, reason="Usuário inativo")
        return
    if user.rule != UserRule.FILIAL:
        websocket.close(code=400, reason="Apenas Filiar pode registrar eventos")
        return
    await websocket.accept()
    # service_event :  InterfaceEventService = get_service_count_event()

    static_websocket: DataEventWebSocketNotifier = get_current_event_websocket()
    await static_websocket.add_connection(websocket, user.filial_id)
    while True:
        try:
            data = await websocket.receive_text()
            log.debug(f"Data received: {data}")
            # await static_websocket.update([EventCountRequest(filial_id=user.filial_id)], user.filial_id)
        except WebSocketDisconnect:
            await static_websocket.remove_connection(user.filial_id)
            break
