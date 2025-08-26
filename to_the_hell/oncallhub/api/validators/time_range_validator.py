

from to_the_hell.oncallhub.api.exceptions import ValidationError, ValidationDurationError
from to_the_hell.oncallhub.domain.value_objects import TimeRange


class TimeRangeValidator:
    """Domain validator for TimeRange value_objects"""
    MIN_DUTY_HOURS = 1
    MAX_DUTY_HOURS = 24

    @classmethod
    def validate_hours(cls, start_hour: int, end_hour: int) -> None:
        """Validate hour values"""
        if not (0 <= start_hour <= 23):
            raise ValidationError(
                f'start hour must be between 0 and 23, got {start_hour}'
            )
        if not (0 <= end hour <= 24):
            raise ValidationError(
                f'end hour must be between 0 and 23, got {end_hour}'
            )

@classmethod
def validate_duration(cls, time_range: TimeRange):
    """Validate duration of duty in hours"""
    if time_range.duration_hours > 12:
        raise ValidationDurationError(
            f''
        )
