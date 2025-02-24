# -*- coding: utf-8 -*-
from logging import getLogger
import datetime
from fastapi import APIRouter, Header, Depends, HTTPException

from src.interfaces import InterfaceStorageService
from src.dto import (
    ResponseTotalCountGrupZone,
    UserPermissionAccessDTO,
    ResponseGrupData,
)
from src.enums import UserRule
from ..core import get_service_storage, rule_require


router = APIRouter()
log = getLogger("controller_count_event")


@router.get("/zone", status_code=200, response_model=ResponseGrupData)
async def get_data_filial_grup_zone(
    current_date: datetime.date,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceStorageService = Depends(get_service_storage),
) -> ResponseGrupData:
    """
    busca dados de uma filial agrupados port zona formato 2024-01-29
    """

    try:
        return storage.get_count_by_filial_grup_zone(user.filial_id, current_date)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/period", status_code=200, response_model=ResponseGrupData)
async def get_periodo(
    start_day: datetime.date,
    end_day: datetime.date,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceStorageService = Depends(get_service_storage),
):
    """
    Busca data dado um periodo de uma filial, se o periodo for um dia agrupa por hora, se for mais de um dia agrupa por dia
    start_day: 2025-01-01
    end_day: 2025-02-01
    """
    try:
        return storage.get_count_by_filial_grup_periodo(
            user.filial_id, start_day, end_day
        )
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))
