from datetime import datetime
from typing import TYPE_CHECKING

from .base_state import IncidentState
from .incident_status import IncidentStatus

if TYPE_CHECKING:
    from to_the_hell.oncallhub.domain.entities import Incident
    from to_the_hell.oncallhub.domain.value_objects import DevopsId


class InProgressIncidentState(IncidentState):
    """State of in progress incident"""

    def assign_to_devops(self, incident: "Incident", devops_id: "DevopsId") -> bool:
        from .assigned import AssignedIncidentState

        incident.assigned_to = devops_id
        incident.assigned_at = datetime.utcnow()
        incident.started_work_at = None
        incident.set_state(AssignedIncidentState())
        return True  # can reassign the devops

    def start_work(self, incident: "Incident") -> bool:
        return False  # work yet started

    def resolve(self, incident: "Incident") -> bool:
        from .resolved import ResolvedIncidentState

        incident.resolved_at = datetime.utcnow()
        incident.set_state(ResolvedIncidentState)
        return True

    def close(self, incident: "Incident") -> bool:
        return False  # need to start by resolving

    def get_status(self) -> IncidentStatus:
        return IncidentState.IN_PROGRESS
