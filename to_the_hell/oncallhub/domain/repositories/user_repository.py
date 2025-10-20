from abc import ABC, abstractmethod

from to_the_hell.oncallhub.domain.entities import User


class BaseUserRepository(ABC):
    """
    Abstract repository for User
    """

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID"""
        pass
