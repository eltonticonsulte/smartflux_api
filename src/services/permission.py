# -*- coding: utf-8 -*-
import logging
from src.interfaces import InterfacePermissionService
from src.dto.permission import RequestCreatePermission
from src.repository import PermissionRepository
from src.mappers import MapperPermission
from src.database import Usuario, PermissaoAcesso
from src.exceptions import ServiceUserExecption, ServiceUserJwtExecption
from ..enums import UserRule


class PermissionService:
    def __init__(self, rep: InterfacePermissionService):
        self.log = logging.getLogger(__name__)
        self.rep = rep

    def create(self, request: RequestCreatePermission) -> int:
        data = MapperPermission.create_to_entity(request)
        return self.rep.create(data)
