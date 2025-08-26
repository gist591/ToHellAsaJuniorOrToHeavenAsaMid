from dataclasses import dataclass
from typing import Optional

from to_the_hell.oncallhub.domain.value_objects import UserId


@dataclass
class User:
    id: UserId
    name: str
    telegram_username: Optional[str] = None
