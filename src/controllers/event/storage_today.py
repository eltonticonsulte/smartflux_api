# -*- coding: utf-8 -*-

from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.enums import UserRule
from src.interfaces import InterfaceStorageTodayService
from src.dto import (
    TotalCount,
    TotalCountGrupZone,
    TotalCountGrupHour,
    UserPermissionAccessDTO,
    TotalCountGrupCamera,
)
from ..core import rule_require, get_storage_today

router = APIRouter()
log = getLogger("controller_count_event")


@router.get("/today/total", status_code=200, response_model=TotalCount)
async def get_data_day(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceStorageTodayService = Depends(get_storage_today),
) -> TotalCount:

    try:
        return count_event.get_count_by_filial(user.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/today/zone", status_code=200, response_model=List[TotalCountGrupZone])
async def get_data_filial_grup_zone(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceStorageTodayService = Depends(get_storage_today),
) -> List[TotalCountGrupZone]:
    try:
        return count_event.get_count_by_filial_count_grup_zone(user.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get("/today/camera", status_code=200, response_model=List[TotalCountGrupCamera])
async def get_today_camera(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceStorageTodayService = Depends(get_storage_today),
) -> List[TotalCountGrupCamera]:
    try:
        return storage.get_count_by_camera_grup_hour(user.filial_id)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, str(error))


@router.get("/today/hour", status_code=200, response_model=List[TotalCountGrupHour])
async def get_data_filial_grup_hour(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceStorageTodayService = Depends(get_storage_today),
) -> List[TotalCountGrupHour]:
    try:
        return count_event.get_count_by_filial_grup_hour(user.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
