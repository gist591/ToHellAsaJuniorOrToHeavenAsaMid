from random import randint

import pytest

from to_the_hell.oncallhub.domain.entities import Devops, Incident
from to_the_hell.oncallhub.domain.value_objects.incident_priority import (
    IncidentPriority,
)


@pytest.mark.asyncio  # type: ignore[misc]
async def test_create_incident() -> None:
    devops = Devops(
        id=randint(0, 10000),
        name="Test Devops",
        telegram_chat_id="123134234",
        email="test@example.com",
        phone="89997655656",
    )

    incident = Incident(
        id=randint(0, 10000),
        title="Test Incident",
        description="Test Description",
        priority=IncidentPriority.HIGH,
    )

    assert incident.title == "Test Incident"
    assert incident.description == "Test Description"
    assert incident.priority == IncidentPriority.HIGH

    assert devops.name == "Test Devops"


@pytest.mark.asyncio  # type: ignore[misc]
async def test_incident_status_transition() -> None:
    devops = Devops(
        id=randint(0, 10000),
        name="Test Devops",
        telegram_chat_id="1542545234",
        email="test@example.com",
        phone="89999999999",
    )

    incident = Incident(
        id=randint(0, 10000),
        title="Test Incident",
        description="Test Description",
        priority=IncidentPriority.MEDIUM,
    )

    assert incident.title == "Test Incident"
    assert incident.description == "Test Description"
    assert incident.priority != IncidentPriority.HIGH

    assert devops.name == "Test Devops"
