# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TITLE: str = "Smartflux"


settings: Settings = Settings()
