from pydantic import BaseModel


class DevopsSchema(BaseModel):
    id: int
    name: str
    telegram_username: str
