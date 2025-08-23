from abc import ABC, abstractmethod

from to_the_hell.oncallhub.domain.entities import Duty, User


class BaseUserRepository(ABC):
    """Abstract repository for User"""

    @abstractmethod
    async def create(self, user: User) -> User:
        pass


class BaseDutyRepository(ABC):
    """Abstract repository for Duty"""

    @abstractmethod
    async def create(self, duty: Duty) -> Duty:
        pass
