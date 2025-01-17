# -*- coding: utf-8 -*-
from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi import WebSocket, WebSocketDisconnect, Request
from src.enums import UserRule
from src.interfaces import (
    InterfaceEventService,
    InterfaceUserService,
)

from src.dto import (
    EventCountRequest,
    EventCountResponse,
    UserPermissionAccessDTO,
)
from ..core import get_service_count_event, rule_require, get_service_user

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
    event_count: InterfaceEventService = get_service_count_event()

    log.debug(user)
    if not user.is_active:
        websocket.close(code=400, reason="Usuário inativo")
        return
    if user.rule != UserRule.FILIAL:
        websocket.close(code=400, reason="Apenas Filiar pode registrar eventos")
        return
    await websocket.accept()
    await event_count.add_websocket_connection(websocket, user.filial_id)
    while True:
        try:
            data = await websocket.receive_text()
            log.debug(f"Data received: {data}")
        except WebSocketDisconnect:
            await event_count.remove_websocket_connection(user.filial_id)
            break


@router.post("/ws/connect")
async def connect(request: Request):
    try:
        print(request)
        # body = await request.body()  # Captura o corpo bruto
        headers = dict(request.headers)
        print(headers)
    except Exception as e:
        print(f"Erro ao processar o payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    return {"statusCode": 200}


@router.post("/ws/disconnect")
async def disconnect(request: Request):
    try:
        headers = dict(request.headers)
    except Exception as e:
        log.debug(f"Erro ao processar o payload: {e}")
    try:

        # body = await request.body()  # Captura o corpo bruto
        headers = dict(request.headers)
        log.debug(headers)
    except Exception as e:
        log.debug(f"Erro ao processar o payload: {e}")

    # Lógica para desconectar o cliente

    return {"statusCode": 200}


@router.post("/ws/default")
async def default_message(request: Request):
    event = await request.json()
    connection_id = event["requestContext"]["connectionId"]
    body = event.get("body", {})
    # Lógica para processar mensagens recebidas
    print(f"Mensagem de {connection_id}: {body}")
    return {"statusCode": 200}


@router.post("/ws/EventCount")
async def event_message(request: Request):
    event = await request.json()
    connection_id = event["requestContext"]["connectionId"]
    body = event.get("body", {})
    # Lógica para processar mensagens recebidas
    print(f"Mensagem de {connection_id}: {body}")
    return {"statusCode": 200}
