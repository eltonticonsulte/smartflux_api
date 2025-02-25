# -*- coding: utf-8 -*-
from logging import getLogger
import datetime
from fastapi import APIRouter, Header, Depends, HTTPException, Query

from src.interfaces import InterfaceStorageService
from src.dto import (
    UserPermissionAccessDTO,
    ResponseGrupData,
    ResponseGrupDataCode,
    RequestVisitor,
)
from src.enums import UserRule, DataFilterTimer
from ..core import get_service_storage, rule_require


router = APIRouter()
log = getLogger("controller_count_event")


@router.get(
    "/zone", status_code=200, response_model=ResponseGrupDataCode, deprecated=True
)
async def get_data_filial_grup_zone(
    current_date: datetime.date,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceStorageService = Depends(get_service_storage),
) -> ResponseGrupDataCode:
    """
    busca dados de uma filial agrupados port zona formato 2024-01-29
    """

    try:
        return storage.get_count_by_filial_grup_zone(user.filial_id, current_date)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get(
    "/period", status_code=200, response_model=ResponseGrupData, deprecated=True
)
async def get_periodo(
    start_day: datetime.date,
    end_day: datetime.date,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceStorageService = Depends(get_service_storage),
):

    try:
        return storage.get_count_by_filial_grup_periodo(
            user.filial_id, start_day, end_day
        )
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))
