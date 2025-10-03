from dataclasses import dataclass
from datetime import datetime
from typing import Any


class IncidentStatus:
    """Base class for incident status"""

    pass


@dataclass
class IncidentCreated(IncidentStatus):
    """Event for incident creation"""

    about_troubles: str
    date: datetime

    def __str__(self) -> str:
        return f"In {self.date} was found incident: {self.about_troubles}"


@dataclass
class IncidentAssigned(IncidentStatus):
    """Represents an incident assignment event"""

    assignee_comment: str
    assigned_at: datetime

    def __str__(self) -> str:
        """Human-readable representation"""
        return f"Incident assigned at {self.assigned_at.isoformat()} | Comment: {self.assignee_comment}"

    def to_timestamp(self) -> float:
        """Convert to Unix timestamp"""
        return self.assigned_at.timestamp()

    def to_iso_string(self) -> str:
        """Convert to ISO 8601 string"""
        return self.assigned_at.isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for API responses"""
        return {
            "event_type": "incident_assigned",
            "assignee_comment": self.assignee_comment,
            "assigned_at": self.assigned_at.isoformat(),
            "timestamp": self.assigned_at.timestamp(),
        }
