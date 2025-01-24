# -*- coding: utf-8 -*-
from logging import getLogger
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from src.interfaces import InterfacePermissionService
from src.dto import (
    UserPermissionAccessDTO,
    RequestCreatePermission,
)
from src.enums import UserRule
from .core import get_service_permission, rule_require


router = APIRouter()
log = getLogger("controller Permission")


@router.post("/create", status_code=200)
async def create(
    request: RequestCreatePermission,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfacePermissionService = Depends(get_service_permission),
):
    try:
        result = service.create(request)
        return result
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))
