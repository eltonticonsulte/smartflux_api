# -*- coding: utf-8 -*-
from logging import getLogger
import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse

from src.interfaces import InterfaceVisitorService
from src.dto import (
    UserPermissionAccessDTO,
    ResponseGrupData,
    ResponseGrupDataLabel,
    RequestVisitorDate,
    RequestVisitorLabel,
    ResponseTotalCount,
    RequestVisitorGrupDate,
)
from src.enums import UserRule, FlagGrupDate, FlagGrupLabel
from .core import get_service_storage, rule_require


router = APIRouter()
log = getLogger("controller_count_visitor")


@router.get("/date", status_code=200, response_model=ResponseGrupData)
async def get_visitor_grup_data(
    start_date: datetime.date = Query(datetime.date.today()),
    end_date: Optional[datetime.date] = None,
    grup: Optional[FlagGrupDate] = Query(FlagGrupDate.AUTO_SELECT),
    zone: Optional[str] = Query(None),
    device: Optional[str] = Query(None),
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceVisitorService = Depends(get_service_storage),
):
    """
    Busca com base em data.

    Se apenas start_date é informado, busca o dia passado.

    Se as duas datas forem informadas, busca o periodo informado.

    Se grup não for informado, o agrupamento é calculado automaticamente, pro hora se o periodo for um dia.

    Se zone for informado, agrupa por zone.

    Se device for informado, agrupa por device.
    """
    try:
        data = RequestVisitorDate(
            start_date=start_date,
            end_date=end_date,
            grup=grup,
            zone=zone,
            device=device,
        )
        return storage.get_count_visitor(user.filial_id, data)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/label", status_code=200, response_model=ResponseGrupDataLabel)
async def get_visitor_grup_label(
    start_date: datetime.date = Query(datetime.date.today()),
    end_date: Optional[datetime.date] = None,
    grup: Optional[FlagGrupLabel] = Query(FlagGrupLabel.ZONE),
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceVisitorService = Depends(get_service_storage),
):
    """
    Busca com base em grup.

    Se apenas start_date é informado, busca o dia passado.

    Se as duas datas forem informadas, busca o periodo informado.

    Grup, define a base de agrupamento.
    """
    try:
        data = RequestVisitorLabel(
            start_date=start_date,
            end_date=end_date,
            grup=grup,
        )
        return storage.get_count_visitor_label(user.filial_id, data)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/report/grup", status_code=200, response_class=PlainTextResponse)
async def get_report_zone_grup(
    start_date: datetime.date = Query(datetime.date.today()),
    end_date: Optional[datetime.date] = None,
    grup: Optional[FlagGrupDate] = Query(FlagGrupDate.AUTO_SELECT),
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceVisitorService = Depends(get_service_storage),
):
    """
    Busca com base em grup, retorna no formato text csv.

    Se apenas start_date é informado, busca o dia passado.

    Se as duas datas forem informadas, busca o periodo informado.

    Grup, define a base de agrupamento.
    """
    try:
        data = RequestVisitorGrupDate(
            start_date=start_date,
            end_date=end_date,
            grup=grup,
        )
        return storage.get_count_visitor_report(user.filial_id, data)
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/total", status_code=200, response_model=ResponseTotalCount)
async def get_data_day(
    date: Optional[datetime.date] = datetime.date.today(),
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceVisitorService = Depends(get_service_storage),
) -> ResponseTotalCount:
    """
    Busca somatória de visitas em um dia.
    """
    try:
        return storage.get_count_by_filial_date(user.filial_id, date)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
