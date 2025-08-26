from datetime import datetime, timezone

import pytest

from to_the_hell.oncallhub.domain.entities import User
from to_the_hell.oncallhub.domain.services import assign_duty
from to_the_hell.oncallhub.domain.value_objects import TimeRange


@pytest.mark.parametrize(
    ("user", "time_range"),
    [
        (
            User(1, "Andrew"),
            TimeRange(
                datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc),
                datetime(2024, 1, 1, 18, 0, tzinfo=timezone.utc)
            )
        ),
    ]

)
def test_assign_duty(user: User, time_range: TimeRange):
    asserted_answer = f"Duty assigned on {time_range} from user {user.name}"

    result = assign_duty(user, time_range)

    assert asserted_answer == result
