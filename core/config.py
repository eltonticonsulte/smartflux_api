# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartFlux API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"

    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: str = str(5432)
    POSTGRES_DB: str = ""
    SECRET_KEY: str = (
        "fddfasdfsftriyoierksdhpgpuhfbap3456l"  # Change this in production
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300

    @property
    def view_connection(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:.........@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = {"env_file": ".env", "case_sensitive": True}


@lru_cache()
def get_settings():
    return Settings()
