from dataclasses import dataclass

from to_the_hell.oncallhub.domain.entities.duty import Duty
from to_the_hell.oncallhub.domain.value_objects import IncidentId, Priority, TimeRange


@dataclass
class Incident:
    """
    Incident in system
    """

    id: IncidentId
    description: str
    time_range: TimeRange
    status: bool
    priority: Priority | None = None
    assigned_duty: Duty | None = None

    def is_active(self) -> bool:
        """Incident is active?"""
        return self.status

    def close(self) -> None:
        """Close incident"""
        self.status = False

    def escalate(self) -> None:
        """
        Escalation
        """
        if self.priority:
            pass
