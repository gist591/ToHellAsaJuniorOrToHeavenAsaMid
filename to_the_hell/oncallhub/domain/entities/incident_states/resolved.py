from datetime import datetime
from typing import TYPE_CHECKING

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
        incident.assigned_at = datetime.utcnow()
        incident.resolved_at = None
        incident.set_state(AssignedIncidentState())
        return True  # can reassign the devops

    def start_work(self, incident: "Incident") -> bool:
        from in_progress import InProgressIncidentState

        incident.resolved_at = None
        incident.started_work_at = datetime.utcnow()
        incident.set_state(InProgressIncidentState())
        return True  # reopen incident

    def resolve(self, incident: "Incident") -> bool:
        return False  # incident was resolved yet

    def close(self, incident: "Incident") -> bool:
        from .closed import ClosedIncidentState

        incident.closed_at = (datetime.utcnow(),)
        incident.get_state(ClosedIncidentState)
        return True

    def get_status(self) -> IncidentStatus:
        return IncidentState.RESOLVED
