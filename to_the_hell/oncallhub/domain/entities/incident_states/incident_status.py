from enum import Enum


class IncidentStatus(Enum):
    """Names all statuses"""

    NEW = "new"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
