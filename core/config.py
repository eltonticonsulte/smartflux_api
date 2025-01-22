# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartFlux API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/v1"

    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: str = str(5432)
    DB_NAME: str = ""
    WEBSOCKET_ENDPOINT: str = ""
    AWS_REGION: str = ""
    SECRET_KEY: str = (
        "fddfasdfsftriyoierksdhpgpuhfbap3456l"  # Change this in production
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300

    @property
    def view_connection(self) -> str:
        return f"postgresql://{self.DB_USER}:.........@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = {"env_file": ".env", "case_sensitive": True}


@lru_cache()
def get_settings():
    return Settings()
