from abc import ABC, abstractmethod

from to_the_hell.oncallhub.domain.entities import Devops, Duty, Incident


class BaseDevopsRepository(ABC):
    """Abstract repository for Devops"""

    @abstractmethod
    async def create(self, devops: Devops) -> Devops:
        pass


class BaseDutyRepository(ABC):
    """Abstract repository for Duty"""

    @abstractmethod
    async def create(self, duty: Duty) -> Duty:
        pass


class BaseIncidentRepository(ABC):
    """Abstract repository for Incident"""

    @abstractmethod
    async def create(self, incident: Incident) -> Incident:
        pass
