from typing import Protocol
from uuid import UUID

from to_the_hell.oncallhub.infra.db.models.user import UserORM


class UserRepository(Protocol):
    async def create(
        self, user_id: UUID, name: str,
        telegram_username: str
    ) -> UserORM:
        ...
