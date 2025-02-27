# -*- coding: utf-8 -*-
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from src.interfaces import InterfaceUserService, InterfaceFilialService
from src.dto import ResponseFindUpdate, RequestFindUpdate, ResponseFilial
from .core import get_service_user, get_service_filial, verificar_api_key

router = APIRouter()


log = getLogger("controller Aplication")


@router.post("/license", status_code=200, deprecated=True)
async def check_license(
    data_filial=Depends(verificar_api_key),
    service: InterfaceUserService = Depends(get_service_user),
):
    try:
        pass
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.post("/zipe_file", status_code=200)
async def get_file_zip(
    data_filial: ResponseFilial = Depends(verificar_api_key),
    zipe_file: UploadFile = File(...),
    service: InterfaceUserService = Depends(get_service_user),
):

    zip_content = await zipe_file.read()
    log.info(zip_content)
    return JSONResponse(status_code=200, content={"status": "ok"})


@router.get("/find_update", status_code=200, response_model=ResponseFindUpdate)
async def get_update(
    data: RequestFindUpdate = Depends(),
    data_filial: ResponseFilial = Depends(verificar_api_key),
    service: InterfaceFilialService = Depends(get_service_filial),
):
    log.info(f"post_status {data}")

    # bucket_name = "meu-bucket"
    # file_key = "minha_app.zip"

    # url = s3.generate_presigned_url('get_object',
    # Params={'Bucket': bucket_name, 'Key': file_key},
    # ExpiresIn=3600)  # Expira em 1 hora

    return ResponseFindUpdate(
        current_version=data.current_version,
        new_version="1.0.0",
        is_update=False,
        url_download=None,
    )
