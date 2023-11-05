from pathlib import Path
from typing import Any, Mapping, Optional

from pydantic import BaseSettings, PostgresDsn, validator

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name = "posthub-backend"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE: str
    POSTGRES_TEST_DATABASE: str = ""
    DATABASE_URL: PostgresDsn = ""
    ALEMBIC_DATABASE_URL: PostgresDsn = ""

    SERVER_PORT: int = 8000
    SERVER_HOST: str = "0.0.0.0"

    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_BACKEND_URL: str = "redis://localhost:6379/1"

    AUTH_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRES: int = 15 * 60
    REFRESH_TOKEN_EXPIRES = 60 * 60 * 24 * 30

    @validator("DATABASE_URL", pre=True)
    def assemble_postgres_db_url(
        cls, v: Optional[str], values: Mapping[str, Any]
    ) -> str:
        if v and isinstance(v, str):
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=str(values["POSTGRES_PORT"]),
                path=f'/{values["POSTGRES_DATABASE"]}',
            )
        )

    @validator("ALEMBIC_DATABASE_URL", pre=True)
    def assemble_alembic_database_url(
        cls, v: Optional[str], values: Mapping[str, Any]
    ) -> str:
        if v and isinstance(v, str):
            return v

        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                user=values["POSTGRES_USER"],
                password=values["POSTGRES_PASSWORD"],
                host=values["POSTGRES_HOST"],
                port=str(values["POSTGRES_PORT"]),
                path=f'/{values["POSTGRES_DATABASE"]}',
            )
        )

    class Config:
        env_file = ".env"


settings = Settings()
