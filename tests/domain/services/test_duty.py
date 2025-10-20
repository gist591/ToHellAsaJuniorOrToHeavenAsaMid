from datetime import UTC, datetime, timedelta
from random import randint

import pytest

from to_the_hell.oncallhub.domain.entities import Devops, Duty
from to_the_hell.oncallhub.domain.repositories import BaseDutyRepository


class FakeDutyRepository(BaseDutyRepository):
    """Fake repository for testing"""

    def __init__(self) -> None:
        self.duties: list[Duty] = []

    async def create(self, duty: Duty) -> Duty:
        """Create duty in memory"""
        duty.id = randint(0, 100000)
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

    devops = Devops(
        id=randint(0, 100000),
        name="Test Devops",
        telegram_username="@hello",
        email="test@example.com",
        phone="8999999999",
    )
    duty_id = randint(0, 100000)

    duty = Duty(
        id=duty_id,
        devops_id=devops.id or randint(0, 100000),
        start_time=datetime.now(tz=UTC),
        end_time=datetime.now(tz=UTC) + timedelta(hours=8),
        status=True,
    )

    created_duty = await repo.create(duty)

    assert created_duty.id is not None
    assert created_duty.devops_id == duty.devops_id
    assert created_duty.status is True
