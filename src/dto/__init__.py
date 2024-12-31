# -*- coding: utf-8 -*-
from .user import (
    AuthUserResponse,
    CreateUserRequest,
    AuthUserRequest,
    GetUserResponse,
)
from .empresa import (
    CreateEmpresaRequest,
    GetEmpresaResponse,
    UpdateEmpresaRequest,
)
from .filial import (
    CreateFilialRequest,
    GetFilialResponse,
    UpdateFilialRequest,
)
from .zone import (
    CreateZoneRequest,
    GetZoneResponse,
    UpdateZoneRequest,
)
from .camera import (
    CreateCameraRequest,
    GetCameraResponse,
    UpdateCameraRequest,
)

from .event_count import EventCountRequest, EventCountResponse, TotalCount
