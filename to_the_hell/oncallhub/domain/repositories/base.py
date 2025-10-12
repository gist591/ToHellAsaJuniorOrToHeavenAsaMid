from abc import ABC, abstractmethod
from uuid import UUID

from to_the_hell.oncallhub.domain.entities import Devops, Duty, Incident


class BaseDutyRepository(ABC):
    """Abstract repository for Duty"""

    @abstractmethod
    async def create(self, duty: Duty) -> Duty:
        pass

    @abstractmethod
    async def get_current_duty(self) -> Duty | None:
        pass

    @abstractmethod
    async def get_all_duties(self) -> list[Duty]:
        pass


class BaseDevopsRepository(ABC):
    """Abstract repository for Devops"""

    @abstractmethod
    async def create(self, devops: Devops) -> Devops:
        pass


class BaseIncidentRepository(ABC):
    """Abstract repository for Incident"""

    @abstractmethod
    async def create(self, incident: Incident) -> Incident:
        pass

    @abstractmethod
    async def get_all_incidents(
        self,
        limit: int | None = None,
        offset: int | None = None,
        status: str | None = None,
        assigned_to: UUID | None = None,
    ) -> list[Incident]:
        pass
