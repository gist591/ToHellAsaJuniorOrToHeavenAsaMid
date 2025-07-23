from uuid import UUID
from datetime import datetime

from to_the_hell.oncallhub.domain.utils.properties_from_models import make_property


class Duty:
    id = make_property('id')
    name = make_property('name')
    user_id = make_property('user_id')
    start_time = make_property('start_time')
    end_time = make_property('end_time')
    status = make_property('status')

    def __init__(self, id: UUID, name: str, user_id: UUID, start_time: datetime, end_time: datetime, status: bool):
        self._id = id
        self._name = name
        self._user_id = user_id
        self._start_time = start_time
        self._end_time = end_time
        self._status = status

    def is_active(self) -> bool:
        return self._status
