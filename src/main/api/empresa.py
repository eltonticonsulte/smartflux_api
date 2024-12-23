# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, Depends
from typing_extensions import Annotated
from fastapi.responses import JSONResponse
from ..composers import CreateEmpresaComposer, EmpresaComposer
from .core import auth2_scheme

router = APIRouter()


@router.post("/create", status_code=201)
async def create(
    empresa: Annotated[CreateEmpresaComposer, Depends()],
    token: str = Depends(auth2_scheme),
):
    if not token:
        raise HTTPException(401, detail="Unauthorized")

    try:
        id_empresa = empresa.create()
        return JSONResponse(status_code=201, content={"id_empresa": id_empresa})
    except Exception as error:
        raise HTTPException(422, detail=str(error))


@router.get("/all")
async def get_all(
    controller: Annotated[EmpresaComposer, Depends()],
    token: str = Depends(auth2_scheme),
):
    if not token:
        raise HTTPException(401, detail="Unauthorized")
    result = controller.get_all()
    return JSONResponse(status_code=200, content=result)
