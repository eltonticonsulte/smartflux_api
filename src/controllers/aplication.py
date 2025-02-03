# -*- coding: utf-8 -*-
import uuid
from fastapi import APIRouter, Header, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from src.interfaces import InterfaceUserService, InterfaceFilialService
from .core import get_service_user, get_service_filial
from src.dto import ResponseFindUpdate, RequestFindUpdate

router = APIRouter()
from logging import getLogger

log = getLogger("controller Aplication")


@router.post("/license", status_code=200, deprecated=True)
async def check_license(
    token: uuid.UUID = Header(...),
    service: InterfaceUserService = Depends(get_service_user),
):
    try:
        pass
    except Exception as error:
        raise HTTPException(500, detail=str(error))


@router.post("/zipe_file", status_code=200)
async def get_file_zip(
    token: uuid.UUID = Header(...),
    zipe_file: UploadFile = File(...),
    service: InterfaceUserService = Depends(get_service_user),
):

    zip_content = await zipe_file.read()
    log.info(zip_content)
    return JSONResponse(status_code=200, content={"status": "ok"})


@router.get("/find_update", status_code=200, response_model=ResponseFindUpdate)
async def post_update(
    data: RequestFindUpdate,
    token: uuid.UUID = Header(...),
    service: InterfaceFilialService = Depends(get_service_filial),
):
    log.info(f"post_status {data}")
    nameuser = service.check_token(token)
    # bucket_name = "meu-bucket"
    # file_key = "minha_app.zip"

    # url = s3.generate_presigned_url('get_object',
    # Params={'Bucket': bucket_name, 'Key': file_key},
    # ExpiresIn=3600)  # Expira em 1 hora

    return JSONResponse(status_code=200, content={"status": "ok", "name": nameuser})
