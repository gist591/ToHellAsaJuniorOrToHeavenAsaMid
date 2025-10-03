from datetime import UTC, datetime

from to_the_hell.oncallhub.domain.entities import Incident
from to_the_hell.oncallhub.domain.events.incidents_events import (
    IncidentAssigned,
)

MESSAGE_INCIDENT_ASSIGNED = "incident is assigned"
MESSAGE_INCIDENT_IN_WORK = "incident in work"
MESSAGE_INCIDENT_CREATED = "incident is created, waiting assign of user"


def check_status_of_incident(incident: Incident) -> str:
    """Check status of incident"""
    if hasattr(incident, "incident_assigned") and incident.incident_assigned:
        return MESSAGE_INCIDENT_ASSIGNED

    if hasattr(incident, "assigned_duty") and incident.assigned_duty:
        return MESSAGE_INCIDENT_IN_WORK

    if hasattr(incident, "is_active") and incident.is_active():
        return MESSAGE_INCIDENT_IN_WORK

    return MESSAGE_INCIDENT_CREATED


def close_incident(incident: Incident, comment_of_user: str = "") -> str:
    """Close incident with comment"""
    if hasattr(incident, "is_active") and incident.is_active():
        return "it is yet active"

    if hasattr(incident, "incident_assigned"):
        incident.incident_assigned = IncidentAssigned(
            comment_of_user, datetime.now(tz=UTC)
        )

    return MESSAGE_INCIDENT_ASSIGNED
