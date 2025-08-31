from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from to_the_hell.oncallhub.domain.value_objects import DevopsId

if TYPE_CHECKING:
    from to_the_hell.oncallhub.domain.entities.incident import Incident
    from to_the_hell.oncallhub.domain.entities.incident_states.incident_status import (
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
    def resolve(self, incident: "Incident", resolution) -> bool:
        pass

    def close(self, incident: "Incident") -> bool:
        pass

    @abstractmethod
    def get_status(self) -> "IncidentStatus":
        pass
