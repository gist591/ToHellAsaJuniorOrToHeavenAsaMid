from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore[misc]
    """Настройки приложения"""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    DATABASE_URL: str
    DATABASE_ECHO: bool = False

    APP_NAME: str = "OnCall Hub"
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-change-in-production"

    API_PREFIX: str = "/api/v1"

    # ============ CELERY ============
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: list[str] = ["json"]
    CELERY_TIMEZONE: str = "UTC"
    CELERY_ENABLE_UTC: bool = True
    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_TASK_TIME_LIMIT: int = 30 * 60
    CELERY_TASK_SOFT_TIME_LIMIT: int = 25 * 60


settings = Settings()
