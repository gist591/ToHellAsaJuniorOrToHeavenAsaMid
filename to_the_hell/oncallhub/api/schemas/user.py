from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):  # type: ignore[misc]
    id: UUID
    name: str
    telegram_username: str
