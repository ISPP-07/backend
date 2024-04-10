import secrets
from pathlib import Path
from typing import Any, ClassVar, List, Optional, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, MongoDsn, ValidationInfo, field_validator

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

    BACKEND_CORS_ORIGINS: List[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(
            cls, v: Union[str, List[str], List[AnyHttpUrl]]) -> List[AnyHttpUrl]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(f"Invalid input for BACKEND_CORS_ORIGINS: {v}")

    MONGO_HOST: str | None = None
    MONGO_USER: str | None = None
    MONGO_PASSWORD: str | None = None
    MONGO_PORT: int | None = None
    MONGO_DB: str
    MONGO_DATABASE_URI: Optional[MongoDsn] | str = None

    @field_validator("MONGO_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(
            cls,
            v: Optional[str],
            values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return MongoDsn.build(  # pylint: disable=E1101
            scheme="mongodb",
            username=values.data.get("MONGO_USER"),
            password=values.data.get("MONGO_PASSWORD"),
            host=values.data.get("MONGO_HOST"),
            port=values.data.get("MONGO_PORT"),
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

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')


settings = Settings()
