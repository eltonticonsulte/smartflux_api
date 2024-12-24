# -*- coding: utf-8 -*-
from fastapi.security import OAuth2PasswordBearer

auth2_admin = OAuth2PasswordBearer(tokenUrl="api/user/login")
auth2_camera = OAuth2PasswordBearer(tokenUrl="api/camera/login")
