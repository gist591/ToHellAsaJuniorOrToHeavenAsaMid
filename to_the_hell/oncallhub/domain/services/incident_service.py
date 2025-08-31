from datetime import datetime

from to_the_hell.oncallhub.domain.entities import Incident
from to_the_hell.oncallhub.domain.events.incidents_events import (
    IncidentAssigned,
)

MESSAGE_INCIDENT_ASSIGNED = "incident is assigned"
MESSAGE_INCIDENT_IN_WORK = "incident in work"
MESSAGE_INCIDENT_CREATED = "incident is created, waiting assign of user"


def check_status_of_incident(incident: Incident) -> str:
    if incident.incident_assigned:
        return MESSAGE_INCIDENT_ASSIGNED
    if incident.assigned_duty:
        return MESSAGE_INCIDENT_IN_WORK
    return MESSAGE_INCIDENT_CREATED


def close_incident(incident: Incident, comment_of_user: str = "") -> str:
    if incident.is_active() == "incident is assigned":
        return "it is yet assigned"
    incident.incident_assigned = IncidentAssigned(comment_of_user, datetime.now())
    return MESSAGE_INCIDENT_ASSIGNED
