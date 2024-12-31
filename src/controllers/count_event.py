# -*- coding: utf-8 -*-
import uuid
from fastapi import APIRouter, Header
from fastapi import APIRouter, Depends, HTTPException

from src.interfaces import (
    InterfaceFilialService,
    InterfaceCameraService,
    InterfaceEventCountService,
)
from .core import get_service_filial, get_service_camera, get_service_count_event
from src.dto import (
    EventCountRequest,
    EventCountResponse,
    TotalCount,
    TotalCountGrupZone,
)

router = APIRouter()

from typing import List


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
