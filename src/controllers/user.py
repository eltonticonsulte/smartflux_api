# -*- coding: utf-8 -*-
from logging import getLogger
from typing import List
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from src.interfaces import InterfaceUserService
from src.dto import (
    ResponseAuthUser,
    RequestAuthUser,
    RequestCreateUser,
    UserPermissionAccessDTO,
)
from src.enums import UserRule
from .core import auth2_admin, get_service_user, rule_require


router = APIRouter()
log = getLogger("controller user")


@router.post("/login", response_model=ResponseAuthUser, status_code=200)
async def get_login(
    auth: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: InterfaceUserService = Depends(get_service_user),
):
    try:
        result: ResponseAuthUser = service.auth_user(
            RequestAuthUser(username=auth.username, password=auth.password)
        )
        return result
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.post("/create", status_code=200)
async def create(
    request: RequestCreateUser,
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceUserService = Depends(get_service_user),
):
    try:
        result: ResponseAuthUser = service.create(request)
        return result
    except Exception as error:
        log.error("error", exc_info=error)
        raise HTTPException(500, detail=str(error))


@router.get("/status", status_code=200, response_model=UserPermissionAccessDTO)
async def get_status(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.FILIAL)),
):
    return user


@router.get("/all", status_code=200, response_model=List[ResponseAuthUser])
async def get_all(
    user: UserPermissionAccessDTO = Depends(rule_require(UserRule.ADMIN)),
    service: InterfaceUserService = Depends(get_service_user),
):
    try:
        result: List[ResponseAuthUser] = service.get_all()
        return result
    except Exception as error:
        raise HTTPException(500, detail=str(error))
