# -*- coding: utf-8 -*-

from logging import getLogger
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.enums import UserRule
from src.interfaces import InterfaceStorageTodayService
from src.dto import (
    ResponseTotalCount,
    ResponseTotalCountGrupZone,
    ResponseTotalCountGrupHour,
    UserPermissionAccessDTO,
    ResponseTotalCountGrupCamera,
    ResponseGrupData,
)
from ..core import rule_require, get_storage_today

router = APIRouter()
log = getLogger("controller_count_event")


@router.get("/today/total", status_code=200, response_model=ResponseTotalCount)
async def get_data_day(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceStorageTodayService = Depends(get_storage_today),
) -> ResponseTotalCount:

    try:
        return count_event.get_count_by_filial(user.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get(
    "/today/zone", status_code=200, response_model=List[ResponseTotalCountGrupZone]
)
async def get_data_filial_grup_zone(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceStorageTodayService = Depends(get_storage_today),
) -> List[ResponseTotalCountGrupZone]:
    try:
        return count_event.get_count_by_filial_grup_zone(user.filial_id)
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.get(
    "/today/camera", status_code=200, response_model=List[ResponseTotalCountGrupCamera]
)
async def get_today_camera(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceStorageTodayService = Depends(get_storage_today),
) -> List[ResponseTotalCountGrupCamera]:
    try:
        return storage.get_count_by_camera_grup_hour(user.filial_id)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, str(error))


@router.get("/today/hour", status_code=200, response_model=ResponseGrupData)
async def get_data_filial_grup_hour(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceStorageTodayService = Depends(get_storage_today),
) -> ResponseGrupData:
    try:

        return count_event.get_count_by_filial_grup_hour(user.filial_id)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/today/hour/zona/{name}", status_code=200, response_model=ResponseGrupData)
async def get_data_filial_zona_grup_hour(
    zona: str,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceStorageTodayService = Depends(get_storage_today),
) -> ResponseGrupData:
    """
    busca dados do dia atual de uma filial e zona agrupados por hora
    """
    try:
        return count_event.get_count_by_filial_zone_grup_hour(user.filial_id, zona)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get(
    "/today/hour/device/{name}", status_code=200, response_model=ResponseGrupData
)
async def get_data_filial_camera_grup_hour(
    device: str,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    count_event: InterfaceStorageTodayService = Depends(get_storage_today),
) -> ResponseGrupData:
    """
    busca dados do dia atual de uma filial e camera agrupados por hora
    """

    try:
        return count_event.get_count_by_filial_camera_grup_hour(user.filial_id, device)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))
