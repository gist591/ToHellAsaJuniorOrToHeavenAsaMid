from dataclasses import dataclass
from uuid import UUID


@dataclass
class Devops:
    id: UUID
    name: str
    telegram_username: str
    email: str
    phone: str
