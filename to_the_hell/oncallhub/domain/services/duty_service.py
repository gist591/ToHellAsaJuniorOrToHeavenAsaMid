from datetime import datetime

from to_the_hell.oncallhub.domain.models import User


def assign_duty(user: User, start_time: datetime, end_time: datetime):


    return f"Успешно назначено дежурство с {start_time} до {end_time} сотрудника {user.name}"
