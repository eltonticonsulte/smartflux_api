# -*- coding: utf-8 -*-
from typing import List
import uuid
import datetime
from fastapi import APIRouter, Header
from fastapi import APIRouter, Depends, HTTPException

from src.interfaces import InterfaceFilialService, InterfaceEventCountStorageService
from .core import get_service_filial, get_service_count_event_storage
from src.dto import TotalCountGrupZone

router = APIRouter()


@router.get(
    "/data/filial/grup-zone", status_code=200, response_model=List[TotalCountGrupZone]
)
async def get_data_filial_grup_zone(
    date: datetime.date,
    token: uuid.UUID = Header(...),
    filial: InterfaceFilialService = Depends(get_service_filial),
    storage: InterfaceEventCountStorageService = Depends(
        get_service_count_event_storage
    ),
) -> List[TotalCountGrupZone]:
    """
    busca dados de uma filial agrupados port zona
    """
    current_filial = None
    try:
        current_filial = filial.get_by_token(token)
    except Exception as error:
        raise HTTPException(401, detail=str(error))
    filial_id = current_filial.filial_id
    try:
        return storage.get_count_by_filial_count_grup_zone(filial_id, date)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
