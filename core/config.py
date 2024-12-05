# -*- coding: utf-8 -*-
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartFlux API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: str = ""
    POSTGRES_DB: str = ""

    @property
    def DATABASE_URL(self) -> str:
        if os.getenv("TESTING"):
            return "sqlite:///:memory:"
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = {"env_file": ".env", "case_sensitive": True}


@lru_cache()
def get_settings():
    return Settings()
