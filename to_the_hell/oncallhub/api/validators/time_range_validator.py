from to_the_hell.oncallhub.api.exceptions import (
    ValidationDurationError,
    ValidationError,
)
from to_the_hell.oncallhub.domain.value_objects import TimeRange


class TimeRangeValidator:
    """Domain validator for TimeRange value_objects"""

    MIN_HOUR = 0
    MAX_START_HOUR = 23
    MAX_END_HOUR = 24
    MAX_DURATION = 12

    @classmethod
    def validate_hours(cls, start_hour: int, end_hour: int) -> None:
        """Validate hour values"""
        if not (cls.MIN_HOUR <= start_hour <= cls.MAX_START_HOUR):
            raise ValidationError(
                f"start hour must be between 0 and 23, got {start_hour}"
            )
        if not (cls.MIN_HOUR <= end_hour <= cls.MAX_END_HOUR):
            raise ValidationError(f"end hour must be between 0 and 23, got {end_hour}")

    @classmethod
    def validate_duration(cls, time_range: TimeRange) -> None:
        """Validate duration of duty in hours"""
        if time_range.duration_hours > cls.MAX_DURATION:
            raise ValidationDurationError(
                f"Duty duration cannot exceed {cls.MAX_DURATION} hours, "
                f"got {time_range.duration_hours:.2f} hours"
            )
