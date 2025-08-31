from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from to_the_hell.oncallhub.domain.entities import Devops, Duty
from to_the_hell.oncallhub.domain.repositories import BaseDutyRepository


class FakeDutyRepository(BaseDutyRepository):
    def __init__(self):
        self.duties = []

    async def create(self, duty: Duty) -> Duty:
        duty.id = uuid4()
        self.duties.append(duty)
        return duty


@pytest.mark.asyncio
async def test_create_duty():
    repo = FakeDutyRepository()

    devops = Devops(name="Test Devops", email="test@example.com")

    duty = Duty(
        devops_id=devops.id or uuid4(),
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=8),
        status=True,
    )

    created_duty = await repo.create(duty)

    assert created_duty.id is not None
    assert created_duty.devops_id == duty.devops_id
    assert created_duty.status is True
