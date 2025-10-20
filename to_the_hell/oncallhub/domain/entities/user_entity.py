from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """
    User domain entity
    """

    username: str
    email: str
    hashed_password: str
    id: int | None = None
    created_at: datetime | None = None
    is_active: bool = True
