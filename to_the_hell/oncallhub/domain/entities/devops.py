from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Devops:
    name: str
    email: str
    phone: str | None = None
    created_at: datetime | None = None
    id: UUID | None = None
