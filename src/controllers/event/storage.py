# -*- coding: utf-8 -*-
from logging import getLogger
import datetime
from typing import Optional
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


@router.get("/zone", status_code=200, response_model=ResponseGrupDataCode)
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
    end_day: 2025-01-31
    """
    try:
        return storage.get_count_by_filial_grup_periodo(
            user.filial_id, start_day, end_day
        )
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/visitors", status_code=200, response_model=ResponseGrupData)
async def get_visitor(
    start_date: datetime.date = Query(...),
    end_date: Optional[datetime.date] = None,
    grup: Optional[DataFilterTimer] = Query(DataFilterTimer.UNDEFINED),
    zone: Optional[str] = Query(None),
    device: Optional[str] = Query(None),
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceStorageService = Depends(get_service_storage),
):
    """
    Busca data dado um periodo de uma filial, se o periodo for um dia agrupa por hora, se for mais de um dia agrupa por dia
    start_day: 2025-01-01
    end_day: 2025-01-31
    """
    try:
        data = RequestVisitor(
            start_data=start_date,
            end_data=end_date,
            grup=grup,
            zone=zone,
            device=device,
        )
        return storage.get_count_visitor(user.filial_id, data)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))
