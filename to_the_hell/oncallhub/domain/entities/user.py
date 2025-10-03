from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    username: str
    email: str
    hashed_password: str
    id: UUID | None = None
    created_at: datetime | None = None
    is_active: bool = True
