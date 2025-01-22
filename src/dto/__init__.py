# -*- coding: utf-8 -*-
from .user import (
    AuthUserResponse,
    CreateUserRequest,
    AuthUserRequest,
    GetUserResponse,
    UserPermissionAccessDTO,
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

from .camera import (
    CreateCameraRequest,
    GetCameraResponse,
    UpdateCameraRequest,
)

from .event_count import (
    EventCountRequest,
    EventCountResponse,
    TotalCount,
    EventCountDataValidate,
)
from .event_count_storage import (
    TotalCountGrupZone,
    TotalCountGrupHour,
    TotalCountGrupCamera,
    TotalCountGroupDay,
)
from .permission import CreatePermissionRequest, DataPermission, PermissionResponse
from .aws_websocket import EventCountSendWebsocket
