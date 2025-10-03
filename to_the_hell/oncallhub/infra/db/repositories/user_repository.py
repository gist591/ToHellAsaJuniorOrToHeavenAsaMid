from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from to_the_hell.oncallhub.domain.entities.user import User
from to_the_hell.oncallhub.domain.repositories.user_repository import BaseUserRepository


class PostgresUserRepository(BaseUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        return None
