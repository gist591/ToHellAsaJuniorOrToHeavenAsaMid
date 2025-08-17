from datetime import datetime, timezone

import pytest

from to_the_hell.oncallhub.domain.models import User
from to_the_hell.oncallhub.domain.services import assign_duty


@pytest.mark.parametrize(
    ("user", "start_time", "end_time"),
    [
        (
            User(1, "Andrew"),
            datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc),
            datetime(2024, 1, 1, 18, 0, tzinfo=timezone.utc)
        ),
    ]

)
def test_assign_duty(user: User, start_time:datetime, end_time: datetime):
    asserted_answer = f"Успешно назначено дежурство с {start_time} до {end_time} сотрудника {user.name}"

    result = assign_duty(user, start_time, end_time)

    assert asserted_answer == result
