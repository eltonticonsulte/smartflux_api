# -*- coding: utf-8 -*-
from typing import List
import uuid
from fastapi import APIRouter, Header, Depends, HTTPException
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.interfaces import (
    InterfaceFilialService,
    InterfaceCameraService,
    InterfaceEventCountService,
    InterfaceUserService,
)

from src.dto import (
    EventCountRequest,
    EventCountResponse,
    TotalCount,
    TotalCountGrupZone,
    TotalCountGrupHour,
)
from .core import (
    get_service_filial,
    get_service_camera,
    get_service_count_event,
    auth2_admin,
    get_service_user,
)

router = APIRouter()


@router.post("/count", status_code=201, response_model=List[EventCountResponse])
async def insert_event(
    request: List[EventCountRequest],
    token: uuid.UUID = Header(...),
    camera: InterfaceCameraService = Depends(get_service_camera),
    filial: InterfaceFilialService = Depends(get_service_filial),
    count_event: InterfaceEventCountService = Depends(get_service_count_event),
) -> List[EventCountResponse]:
    current_filial = None
    try:
        current_filial = filial.get_by_token(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))

    try:
        channels_id: List[uuid.UUID] = camera.get_channel_by_filial(
            current_filial.filial_id
        )
        result: List[EventCountResponse] = count_event.insert_pull(request, channels_id)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/total/current-today", status_code=200, response_model=TotalCount)
async def get_data_day(
    token: uuid.UUID = Header(...),
    filial: InterfaceFilialService = Depends(get_service_filial),
    count_event: InterfaceEventCountService = Depends(get_service_count_event),
) -> TotalCount:
    current_filial = None
    try:
        current_filial = filial.get_by_token(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))

    try:
        return count_event.get_count_by_filial(current_filial.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get(
    "/total/grup-zone", status_code=200, response_model=List[TotalCountGrupZone]
)
async def get_data_filial_grup_zone(
    token: uuid.UUID = Header(...),
    filial: InterfaceFilialService = Depends(get_service_filial),
    count_event: InterfaceEventCountService = Depends(get_service_count_event),
) -> List[TotalCountGrupZone]:
    current_filial = None
    try:
        current_filial = filial.get_by_token(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))

    try:
        return count_event.get_count_by_filial_count_grup_zone(current_filial.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get(
    "/total/grup-hour", status_code=200, response_model=List[TotalCountGrupHour]
)
async def get_data_filial_grup_hour(
    token: uuid.UUID = Depends(auth2_admin),
    auth: InterfaceUserService = Depends(get_service_user),
    filial: InterfaceFilialService = Depends(get_service_filial),
    count_event: InterfaceEventCountService = Depends(get_service_count_event),
) -> List[TotalCountGrupHour]:
    current_filial = None
    try:
        auth.current_user(token)
        current_filial = filial.get_by_token(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))

    try:
        return count_event.get_count_by_filial_grup_hour(current_filial.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Aceitar conexão do cliente
    await websocket.accept()
    try:
        while True:
            # Receber mensagem do cliente
            data = await websocket.receive_text()
            print(f"Mensagem recebida: {data}")

            # Enviar resposta ao cliente
            await websocket.send_text(f"Você disse: {data}")
    except WebSocketDisconnect:
        print("Conexão WebSocket encerrada")
