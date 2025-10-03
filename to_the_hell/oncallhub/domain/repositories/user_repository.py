from abc import ABC, abstractmethod
from uuid import UUID

from to_the_hell.oncallhub.domain.entities.user import User


class BaseUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        pass
