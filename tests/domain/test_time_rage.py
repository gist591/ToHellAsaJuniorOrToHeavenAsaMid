from typing import Any
import pytest
from datetime import datetime, timezone

from to_the_hell.oncallhub.domain.exceptions import ValidationError, ValidationDurationError
from to_the_hell.oncallhub.domain.value_objects import TimeRange

@pytest.mark.skip(
    reason='in that moment method is not exist'
)
@pytest.mark.parametrize(
    ('start', 'end', 'expected_result'),
    [
        (
            datetime(2024, 1, 1, 18, 25, tzinfo=timezone.utc),
            datetime(2024, 1, 1, 18, 8, tzinfo=timezone.utc),
            ValidationError
        ),
        (
            datetime(2024, 1, 1, 18, 13, tzinfo=timezone.utc),
            datetime(2024, 1, 1, 18, 24, tzinfo=timezone.utc),
            ValidationError
        ),
        (
            datetime(2024, 1, 1, 18, 25, tzinfo=timezone.utc),
            datetime(2024, 1, 1, 18, 24, tzinfo=timezone.utc),
            ValidationError
        ),
        (
            datetime(2024, 1, 1, 18, 0, tzinfo=timezone.utc),
            datetime(2024, 1, 1, 18, 24, tzinfo=timezone.utc),
            ValidationDurationError
        ),
        (
            datetime(2024, 1, 1, 18, 0, tzinfo=timezone.utc),
            datetime(2024, 1, 1, 18, 24, tzinfo=timezone.utc),
            '2024-01-01T18:00:00+00:00 - 2024-01-01T18:24:00+00:00'
        ),
    ]
)
def test_time_range(
    start: datetime,
    end: datetime,
    expected_result: Any
) -> Any:
        if not (isinstance(expected_result, str)): # TODO: if isinstance(expected_result, Exception)
            with pytest.raises(expected_result):
                TimeRange(start, end)
        else:
            assert TimeRange(start, end).__str__() == expected_result
