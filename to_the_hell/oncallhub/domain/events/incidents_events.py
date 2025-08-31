from dataclasses import dataclass
from datetime import datetime


class IncidentStatus:
    """Base class for incident status"""

    pass


@dataclass
class IncidentCreated(IncidentStatus):
    """Time of create incident"""

    about_troubles: str
    date: datetime

    def __str__(self) -> str:
        return f"In {self.date} was found incident: {self.about_troubles}"


@dataclass
class IncidentAssigned(IncidentStatus):
    """Time of assigne incident"""

    comment_of_user: str
    date: datetime

    def __str__(self) -> str:
        return f"In {self.date} was solved incident, comment of user: {self.comment_of_user}"

    def to_str(self) -> float:
        return float(self.date)  # TODO: make it
