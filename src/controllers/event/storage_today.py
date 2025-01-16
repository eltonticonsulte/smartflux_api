# -*- coding: utf-8 -*-

from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.enums import UserRule
from src.interfaces import (
    InterfaceStorageTodayService,
    InterfaceEventService,
    InterfaceUserService,
)
from src.dto import (
    EventCountRequest,
    EventCountResponse,
    TotalCount,
    TotalCountGrupZone,
    TotalCountGrupHour,
    UserPermissionAccessDTO,
)
from ..core import get_service_count_event, rule_require, get_storage_today

router = APIRouter()
log = getLogger("controller_count_event")


@router.get("/total/current-today", status_code=200, response_model=TotalCount)
async def get_data_day(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceStorageTodayService = Depends(get_storage_today),
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
    count_event: InterfaceStorageTodayService = Depends(get_storage_today),
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
    count_event: InterfaceStorageTodayService = Depends(get_storage_today),
) -> List[TotalCountGrupHour]:
    try:
        return count_event.get_count_by_filial_grup_hour(user.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
