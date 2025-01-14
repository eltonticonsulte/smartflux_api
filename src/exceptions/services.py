# -*- coding: utf-8 -*-


class ServiceUserExecption(Exception):
    def __init__(self, message):
        self.message = message


class ServiceUserJwtExecption(Exception):
    def __init__(self, message):
        self.message = message
