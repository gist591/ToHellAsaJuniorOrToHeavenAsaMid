from typing import TYPE_CHECKING

from .base_state import IncidentState
from .incident_status import IncidentStatus

if TYPE_CHECKING:
    from to_the_hell.oncallhub.domain.entities import Incident
    from to_the_hell.oncallhub.domain.value_objects import DevopsId


class ClosedIncidentState(IncidentState):
    """State of closed incident"""

    def assign_to_devops(self, incident: "Incident", devops_id: "DevopsId") -> bool:
        return False

    def start_work(self, incident: "Incident") -> bool:
        return False

    def resolve(self, incident: "Incident") -> bool:
        return False

    def close(self, incident: "Incident") -> bool:
        return False

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.CLOSED
