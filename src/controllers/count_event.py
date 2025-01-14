# -*- coding: utf-8 -*-
from typing import List
from fastapi import APIRouter, Header, Depends, HTTPException
from fastapi import WebSocket, WebSocketDisconnect
from src.enums import UserRule
from src.interfaces import InterfaceTodayStorageService, InterfaceEventService

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
)

router = APIRouter()


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

        result: List[EventCountResponse] = count_event.process_event(request, user)
        return result
    except Exception as error:
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


@router.websocket("/ws/{filial_id}")
async def websocket_endpoint(websocket: WebSocket, filial_id: int):
    await websocket.accept()
    try:
        while True:
            # Receber mensagem do cliente
            data = await websocket.receive_text()
            print(f"Mensagem recebida: {data}")
            await websocket.send_text(f"Você disse: {data}")
    except WebSocketDisconnect:
        print("Conexão WebSocket encerrada")
