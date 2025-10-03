from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from .base_state import IncidentState
from .incident_status import IncidentStatus

if TYPE_CHECKING:
    from to_the_hell.oncallhub.domain.entities import Incident
    from to_the_hell.oncallhub.domain.value_objects import DevopsId


class ResolvedIncidentState(IncidentState):
    """State of resolved incident"""

    def assign_to_devops(self, incident: "Incident", devops_id: "DevopsId") -> bool:
        from .assigned import AssignedIncidentState

        incident.assigned_to = devops_id
        incident.assigned_at = datetime.now(tz=UTC)
        incident.resolved_at = None
        incident.set_state(AssignedIncidentState())
        return True

    def start_work(self, incident: "Incident") -> bool:
        from .in_progress import InProgressIncidentState

        incident.resolved_at = None
        incident.started_work_at = datetime.now(tz=UTC)
        incident.set_state(InProgressIncidentState())
        return True

    def resolve(self, incident: "Incident", resolution: Any | None = None) -> bool:
        return False

    def close(self, incident: "Incident") -> bool:
        from .closed import ClosedIncidentState

        incident.closed_at = datetime.now(tz=UTC)
        incident.set_state(ClosedIncidentState())
        return True

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.RESOLVED
