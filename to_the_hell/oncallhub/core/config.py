from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore[misc]
    """Application settings"""

    # Database
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str

    @property
    def get_database_url(self) -> str:
        """Get async database URL for SQLAlchemy"""
        return (
            f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    DATABASE_ECHO: bool

    # Application
    APP_NAME: str = "OnCall Hub"
    DEBUG: bool
    SECRET_KEY: str
    API_PREFIX: str = "/api/v1"

    # CELERY
    CELERY_REDIS_HOST: str
    CELERY_REDIS_PORT: str
    CELERY_REDIS_PASSWORD: str
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: list[str] = ["json"]
    CELERY_TIMEZONE: str = "UTC"
    CELERY_ENABLE_UTC: bool = True
    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_TASK_TIME_LIMIT: int = 30 * 60
    CELERY_TASK_SOFT_TIME_LIMIT: int = 25 * 60

    @property
    def get_redis_url(self) -> str:
        """Get Celery Redis URL"""
        if self.CELERY_REDIS_PASSWORD:
            return f"redis://:{self.CELERY_REDIS_PASSWORD}@{self.CELERY_REDIS_HOST}:{self.CELERY_REDIS_PORT}/0"
        return f"redis://{self.CELERY_REDIS_HOST}:{self.CELERY_REDIS_PORT}/0"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


settings = Settings()
