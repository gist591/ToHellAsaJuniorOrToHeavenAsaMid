import uuid
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from to_the_hell.oncallhub.domain.entities import Devops, Duty, Incident
from to_the_hell.oncallhub.domain.value_objects.incident_priority import (
    IncidentPriority,
)


def test_devops_creation() -> None:
    """Test devops entity creation"""
    devops = Devops(
        id=uuid.uuid4(),
        name="Test Devops",
        telegram_username="go",
        email="test@example.com",
        phone="+1234567890",
    )

    assert devops.name == "Test Devops"
    assert devops.telegram_username == "go"
    assert devops.email == "test@example.com"
    assert devops.phone == "+1234567890"
    assert devops.id


def test_duty_creation() -> None:
    """Test duty entity creation"""
    devops_id = uuid4()
    duty_id = uuid4()
    start_time = datetime.now(tz=UTC)
    end_time = start_time + timedelta(hours=8)

    duty = Duty(
        id=duty_id,
        devops_id=devops_id,
        start_time=start_time,
        end_time=end_time,
        status=True,
    )

    assert duty.id == duty_id
    assert duty.devops_id == devops_id
    assert duty.start_time == start_time
    assert duty.end_time == end_time
    assert duty.status is True
    assert duty.created_at is None


def test_incident_creation() -> None:
    """Test incident entity creation"""
    incident = Incident(
        id=uuid.uuid4(),
        title="Test Incident",
        description="Test Description",
        priority=IncidentPriority.HIGH,
    )

    assert incident.title == "Test Incident"
    assert incident.description == "Test Description"
    assert incident.priority == IncidentPriority.HIGH
    assert incident.id is None
    assert incident.assigned_id is None
    assert incident.comments == []
