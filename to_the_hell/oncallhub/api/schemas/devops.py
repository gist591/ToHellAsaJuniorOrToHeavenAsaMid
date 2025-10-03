from uuid import UUID

from pydantic import BaseModel


class DevopsSchema(BaseModel):
    id: UUID
    name: str
    telegram_username: str
