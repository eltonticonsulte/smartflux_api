# -*- coding: utf-8 -*-
from .user import (
    AuthUserResponse,
    CreateUserRequest,
    AuthUserRequest,
    CreateUserResponse,
)
from .empresa import (
    CreateEmpresaRequest,
    CreateEmpresaResponse,
    GetEmpresaResponse,
)
from .filial import CreateFilialRequest, CreateFilialResponse, GetFilialResponse
from .zone import CreateZoneRequest, CreateZoneResponse, GetZoneResponse
from .camera import (
    CreateCameraRequest,
    CreateCameraResponse,
    GetCameraResponse,
)

from .event_count import EventCountRequest, EventCountResponse
