from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore[misc]
    """Настройки приложения"""

    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/dbname"
    DATABASE_URL_asyncpg: str = "postgresql+asyncpg://user:pass@localhost/dbname"
    DATABASE_ECHO: bool = False

    APP_NAME: str = "OnCall Hub"
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-change-in-production"

    API_PREFIX: str = "/api/v1"

    REDIS_URL: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


settings = Settings()
