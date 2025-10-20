from sqlalchemy.ext.asyncio import AsyncSession

from to_the_hell.oncallhub.domain.entities import User
from to_the_hell.oncallhub.domain.repositories.user_repository import BaseUserRepository


class PostgresUserRepository(BaseUserRepository):
    """
    PostgreSQL implementation of user repository
    """

    def __init__(self, session: AsyncSession):
        """Initialize repository with async session"""
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by integer ID"""
        return None
