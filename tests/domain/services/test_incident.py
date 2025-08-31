import pytest

from to_the_hell.oncallhub.domain.entities import Devops, Incident
from to_the_hell.oncallhub.domain.value_objects.incident_priority import (
    IncidentPriority,
)


@pytest.mark.asyncio
async def test_create_incident():
    devops = Devops(name="Test Devops", email="test@example.com")

    incident = Incident(
        title="Test Incident",
        description="Test Description",
        priority=IncidentPriority.HIGH,
    )

    assert incident.title == "Test Incident"
    assert incident.description == "Test Description"
    assert incident.priority == IncidentPriority.HIGH


@pytest.mark.asyncio
async def test_incident_status_transition():
    devops = Devops(name="Test Devops", email="test@example.com")

    incident = Incident(
        title="Test Incident",
        description="Test Description",
        priority=IncidentPriority.MEDIUM,
    )
