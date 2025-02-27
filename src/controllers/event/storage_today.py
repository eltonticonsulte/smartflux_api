# -*- coding: utf-8 -*-

from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException
from src.enums import UserRule, FlagGrupLabel
from src.interfaces import InterfaceStorageTodayService, InterfaceStorageService
from src.dto import (
    ResponseTotalCount,
    ResponseTotalCountGrupZone,
    ResponseTotalCountGrupHour,
    UserPermissionAccessDTO,
    ResponseTotalCountGrupCamera,
    ResponseGrupData,
    RequestVisitorLabel,
    ResponseGrupDataLabel,
)
from ..core import rule_require, get_storage_today, get_service_storage

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
