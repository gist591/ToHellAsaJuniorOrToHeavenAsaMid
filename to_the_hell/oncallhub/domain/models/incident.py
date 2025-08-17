from datetime import datetime
from uuid import UUID
from typing import Optional, List

from to_the_hell.oncallhub.domain.models.duty import Duty
from to_the_hell.oncallhub.domain.utils.properties_from_models import make_property


class Incident:
    id = make_property("id")
    description = make_property("description")
    time_start_event = make_property("time_start_event")
    status = make_property("status")

    def __init__(
        self, id: UUID, description: str, time_start_event: datetime,
        status: bool, duties: Optional[List['Duty']] = None
    ):
            self._id = id
            self._description = description
            self._time_start_event = time_start_event
            self._status = status
            self._duties = duties or []

    @property
    def duty(self):
        return self._duty

    @duty.setter
    def duty(self, duty: Duty):
        self._duty.append(duty)

    @duty.deleter
    def duty(self, duty: Duty):
        del self._duty[duty]
