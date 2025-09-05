from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from .base_state import IncidentState
from .incident_status import IncidentStatus

if TYPE_CHECKING:
    from to_the_hell.oncallhub.domain.entities import Incident
    from to_the_hell.oncallhub.domain.value_objects import DevopsId


class NewIncidentState(IncidentState):
    """State of new incident"""

    def assign_to_devops(self, incident: "Incident", devops_id: "DevopsId") -> bool:
        from .assigned import AssignedIncidentState

        incident.assigned_to = devops_id
        incident.assigned_at = datetime.now(tz=UTC)
        incident.set_state(AssignedIncidentState())
        return True

    def start_work(self, incident: "Incident") -> bool:
        return False

    def resolve(self, incident: "Incident", resolution: Any | None = None) -> bool:
        return False

    def close(self, incident: "Incident") -> bool:
        return False

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.NEW
