from abc import ABC, abstractmethod

from to_the_hell.oncallhub.domain.entities import Devops, Duty, Incident


class BaseDutyRepository(ABC):
    """
    Abstract repository for Duty
    """

    @abstractmethod
    async def create(self, duty: Duty) -> Duty:
        """Create new duty"""
        pass

    @abstractmethod
    async def get_current_duty(self) -> Duty | None:
        """Get currently active duty"""
        pass

    @abstractmethod
    async def get_all_duties(self) -> list[Duty]:
        """Get all duties"""
        pass


class BaseDevopsRepository(ABC):
    """
    Abstract repository for Devops
    """

    @abstractmethod
    async def create(self, devops: Devops) -> Devops:
        """Create new devops user"""
        pass


class BaseIncidentRepository(ABC):
    """
    Abstract repository for Incident
    """

    @abstractmethod
    async def create(self, incident: Incident) -> Incident:
        """Create new incident"""
        pass

    @abstractmethod
    async def get_all_incidents(
        self,
        limit: int | None = None,
        offset: int | None = None,
        status: str | None = None,
        assigned_to: int | None = None,
    ) -> list[Incident]:
        """Get all incidents with optional filtering"""
        pass
