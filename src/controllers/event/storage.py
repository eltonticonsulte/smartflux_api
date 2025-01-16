# -*- coding: utf-8 -*-
from typing import List
from logging import getLogger
import datetime
from fastapi import APIRouter, Header, Depends, HTTPException

from src.interfaces import InterfaceStorageService
from src.dto import TotalCountGrupZone, UserPermissionAccessDTO
from src.enums import UserRule
from ..core import get_service_count_event_storage, rule_require


router = APIRouter()
log = getLogger("controller_count_event")


@router.get(
    "/data/filial/grup-zone", status_code=200, response_model=List[TotalCountGrupZone]
)
async def get_data_filial_grup_zone(
    current_date: datetime.date,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
    storage: InterfaceStorageService = Depends(get_service_count_event_storage),
) -> List[TotalCountGrupZone]:
    """
    busca dados de uma filial agrupados port zona
    """

    try:
        return storage.get_count_by_filial_count_grup_zone(user.filial_id, current_date)
    except Exception as error:
        raise HTTPException(500, detail=str(error))
