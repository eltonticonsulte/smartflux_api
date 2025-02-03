# -*- coding: utf-8 -*-
from typing import Optional
from pydantic import BaseModel


class RequestFindUpdate(BaseModel):
    current_version: str


class ResponseFindUpdate(BaseModel):
    current_version: str
    new_version: str
    is_update: bool
    url_download: Optional[str]
