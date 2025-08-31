from datetime import datetime
from typing import TYPE_CHECKING

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
        incident.assigned_at = datetime.utcnow()
        incident.set_state(AssignedIncidentState())
        return True

    def start_work(self, incident: "Incident") -> bool:
        return False  # can't start work not-assigned incident

    def resolve(self, incident: "Incident") -> bool:
        return False  # can't resolve not-assigned incident

    def close(self, incident: "Incident") -> bool:
        return False  # can't close not-assigned incident

    def get_status(self) -> IncidentStatus:
        return IncidentStatus.NEW
