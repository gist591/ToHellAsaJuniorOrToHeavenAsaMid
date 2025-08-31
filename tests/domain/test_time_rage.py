from datetime import UTC, datetime
from typing import Any

import pytest

from to_the_hell.oncallhub.api.exceptions import (
    ValidationDurationError,
    ValidationError,
)
from to_the_hell.oncallhub.domain.value_objects import TimeRange


@pytest.mark.skip(reason="in that moment method is not exist")
@pytest.mark.parametrize(
    ("start", "end", "expected_result"),
    [
        (
            datetime(2024, 1, 1, 18, 25, tzinfo=UTC),
            datetime(2024, 1, 1, 18, 8, tzinfo=UTC),
            ValidationError,
        ),
        (
            datetime(2024, 1, 1, 18, 13, tzinfo=UTC),
            datetime(2024, 1, 1, 18, 24, tzinfo=UTC),
            ValidationError,
        ),
        (
            datetime(2024, 1, 1, 18, 25, tzinfo=UTC),
            datetime(2024, 1, 1, 18, 24, tzinfo=UTC),
            ValidationError,
        ),
        (
            datetime(2024, 1, 1, 18, 0, tzinfo=UTC),
            datetime(2024, 1, 1, 18, 24, tzinfo=UTC),
            ValidationDurationError,
        ),
        (
            datetime(2024, 1, 1, 18, 0, tzinfo=UTC),
            datetime(2024, 1, 1, 18, 24, tzinfo=UTC),
            "2024-01-01T18:00:00+00:00 - 2024-01-01T18:24:00+00:00",
        ),
    ],
)
def test_time_range(start: datetime, end: datetime, expected_result: Any) -> Any:
    if not (
        isinstance(expected_result, str)
    ):  # TODO: if isinstance(expected_result, Exception)
        with pytest.raises(expected_result):
            TimeRange(start, end)
    else:
        assert TimeRange(start, end).__str__() == expected_result
