from to_the_hell.oncallhub.domain.entities import User
from to_the_hell.oncallhub.domain.value_objects import TimeRange

MIN_DUTY_HOURS = 1
MAX_DUTY_HOURS = 24


def assign_duty(user: User, time_range: TimeRange) -> str:
    """
    Assign duty to user

    Args:
        user: user for duty
        time_range: time range of duty

    Returns:

    """
    return f"Duty assigned on {time_range} from user {user.name}"


def validate_duty_assignment(user: User, time_range: TimeRange) -> bool:
    """
    Valisate duty assigment
    """
    if time_range.duration_hours < MIN_DUTY_HOURS:
        raise ValueError(f"Duty must be at least {MIN_DUTY_HOURS} hour long")

    if time_range.duration_hours > MAX_DUTY_HOURS:
        raise ValueError(f"Duty cannot exceed {MAX_DUTY_HOURS} hours")

    return True
