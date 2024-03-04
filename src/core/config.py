from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import secrets
from fastapi import Depends
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, PostgresDsn, validator, ValidationInfo, field_validator
from fastapi.responses import JSONResponse


APP_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):

    APP_DIR: Path = APP_DIR

    CYC_NGO: bool

    ACAT_NGO: bool

    STAGING: bool

    PROJECT_NAME: str

    API_STR: str

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_REFRESH_SECRET_KEY: str = secrets.token_urlsafe(32)

    FIRST_SUPERUSER_USERNAME: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_EMAIL: str

    SERVER_HOST: str
    SERVER_PORT: int

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(
            cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(
            cls,
            v: Optional[str],
            values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            port=values.data.get("POSTGRES_PORT"),
            path=values.data.get("POSTGRES_DB") or ""
        )

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        """Creates dictionary of values to pass to FastAPI app
        as **kwargs.

        Returns:
            dict: This can be unpacked as **kwargs to pass to FastAPI app.
        """

        print(self.STAGING)

        fastapi_kwargs = {
            "title": self.PROJECT_NAME,
            "openapi_url": f"{self.API_STR}/openapi.json",
            "default_response_class": JSONResponse,
        }

        if self.STAGING:
            fastapi_kwargs.update(
                {
                    "openapi_url": None,
                    "openapi_prefix": None,
                    "docs_url": None,
                    "redoc_url": None,
                }
            )
        return fastapi_kwargs

    class Config:
        env_file = ".env"


settings = Settings()
