from pathlib import Path
from typing import Any, List, Optional, Union
import secrets
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, PostgresDsn, ValidationInfo, field_validator
from fastapi.responses import JSONResponse

APP_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):

    APP_DIR: Path = APP_DIR

    CYC_NGO: bool

    ACAT_NGO: bool

    STAGING: bool

    PROJECT_NAME: str

    API_STR: str
    SECRET_KEY: str = secrets.token_urlsafe(32)

    SERVER_HOST: str
    SERVER_PORT: int

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
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
