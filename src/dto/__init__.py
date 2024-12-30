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
    UpdateEmpresaRequest,
)
from .filial import (
    CreateFilialRequest,
    CreateFilialResponse,
    GetFilialResponse,
    UpdateFilialRequest,
)
from .zone import (
    CreateZoneRequest,
    CreateZoneResponse,
    GetZoneResponse,
    UpdateZoneRequest,
)
from .camera import (
    CreateCameraRequest,
    CreateCameraResponse,
    GetCameraResponse,
    UpdateCameraRequest,
)

from .event_count import EventCountRequest, EventCountResponse
