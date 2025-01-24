# -*- coding: utf-8 -*-
from .user import (
    ResponseAuthUser,
    RequestCreateUser,
    RequestAuthUser,
    UserPermissionAccessDTO,
)
from .empresa import (
    RequestCreateEmpresa,
    ResponseEmpresa,
    ResquestUpdateEmpresa,
)
from .filial import (
    RequestCreateFilial,
    ResponseFilial,
    RequestUpdateFilial,
)

from .camera import (
    RequestCreateCamera,
    ResponseCamera,
    RequestUpdateCamera,
    RequestPing,
)

from .event_count import (
    RequestEventCount,
    ResponseEventCount,
    ResponseTotalCount,
    EventCountDataValidate,
)
from .event_count_storage import (
    ResponseTotalCountGrupZone,
    ResponseTotalCountGrupHour,
    ResponseTotalCountGrupCamera,
    ResponseTotalCountGroupDay,
)
from .permission import RequestCreatePermission, ResponsePermission
from .aws_websocket import EventCountSendWebsocket
