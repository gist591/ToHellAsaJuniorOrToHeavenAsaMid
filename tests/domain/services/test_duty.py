from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from to_the_hell.oncallhub.domain.entities import Devops, Duty
from to_the_hell.oncallhub.domain.repositories import BaseDutyRepository


class FakeDutyRepository(BaseDutyRepository):
    """Fake repository for testing"""

    def __init__(self) -> None:
        self.duties: list[Duty] = []

    async def create(self, duty: Duty) -> Duty:
        """Create duty in memory"""
        duty.id = uuid4()
        self.duties.append(duty)
        return duty

    async def get_current_duty(self) -> Duty | None:
        """Get current duty - not implemented for tests"""
        return None

    async def get_all_duties(self) -> list[Duty]:
        """Get all duties - not implemented for tests"""
        return self.duties


@pytest.mark.asyncio  # type: ignore[misc]
async def test_create_duty() -> None:
    """Test duty creation through repository"""
    repo = FakeDutyRepository()

    devops = Devops(name="Test Devops", email="test@example.com")
    duty_id = uuid4()

    duty = Duty(
        id=duty_id,
        devops_id=devops.id or uuid4(),
        start_time=datetime.now(tz=UTC),
        end_time=datetime.now(tz=UTC) + timedelta(hours=8),
        status=True,
    )

    created_duty = await repo.create(duty)

    assert created_duty.id is not None
    assert created_duty.devops_id == duty.devops_id
    assert created_duty.status is True
