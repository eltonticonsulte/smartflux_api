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
    try:
        filial.validate_token(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))

    try:
        channels_id: List[uuid.UUID] = camera.get_all_channels()
        result: List[EventCountResponse] = count_event.insert_pull(request, channels_id)
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))