from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from to_the_hell.oncallhub.domain.value_objects import DevopsId

if TYPE_CHECKING:
    from to_the_hell.oncallhub.domain.entities import Incident
    from to_the_hell.oncallhub.domain.entities.incident_states import (
        IncidentStatus,
    )


class IncidentState(ABC):
    """Abstract Incident state"""

    @abstractmethod
    def assign_to_devops(self, incident: "Incident", devops_id: DevopsId) -> bool:
        pass

    @abstractmethod
    def start_work(self, incident: "Incident") -> bool:
        pass

    @abstractmethod
    def resolve(self, incident: "Incident", resolution: Any = None) -> bool:
        pass

    @abstractmethod
    def close(self, incident: "Incident") -> bool:
        pass

    @abstractmethod
    def get_status(self) -> "IncidentStatus":
        pass
