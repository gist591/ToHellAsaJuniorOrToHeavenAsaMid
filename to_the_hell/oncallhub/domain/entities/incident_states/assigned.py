from datetime import datetime
from typing import TYPE_CHECKING

from .base_state import IncidentState
from .incident_status import IncidentStatus

if TYPE_CHECKING:
    from to_the_hell.oncallhub.domain.entities import Incident
    from to_the_hell.oncallhub.domain.value_objects import DevopsId


class AssignedIncidentState(IncidentState):
    """State of assigned incident"""

    def assign_to_devops(self, incident: "Incident", devops_id: "DevopsId") -> bool:
        incident.assigned_to = devops_id
        incident.assigned_at = datetime.utcnow()
        incident.set_state(AssignedIncidentState())
        return True  # can reassign the devops

    def start_work(self, incident: "Incident") -> bool:
        from .in_progress import InProgressIncidentState

        incident.started_work_at = datetime.utcnow()
        incident.set_state(InProgressIncidentState())
        return True

    def resolve(self, incident: "Incident") -> bool:
        return False  # need to get started

    def close(self, incident: "Incident") -> bool:
        return False  # need to start by resolving

    def get_status(self) -> IncidentStatus:
        return IncidentState.ASSIGNED
