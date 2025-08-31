from datetime import datetime
from uuid import UUID

from to_the_hell.oncallhub.domain.value_objects import DevopsId, IncidentPriority

from .incident_states import IncidentState, NewIncidentState


class Incident:
    """Доменная сущность инцидента"""

    def __init__(
        self,
        title: str,
        description: str,
        priority: "IncidentPriority",
    ):
        self.title = title
        self.description = description
        self.priority = priority
        self.created_at = datetime.utcnow()
        self.status: IncidentState = NewIncidentState()

        self.id: UUID | None = None
        self.assigned_id: UUID | None = None
        self.assigned_at: datetime | None = None
        self.updated_at: datetime | None = None
        self.comments: list[IncidentComment] = []

    def assign_to_devops(self, devops_id: DevopsId) -> None:
        """Назначить инцидент пользователю"""
        self.assigned_id = devops_id
        self.assigned_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def add_comment(self, text: str, user_id: UUID) -> None:
        """Добавить комментарий к инциденту"""
        comment = IncidentComment(
            text=text, user_id=user_id, created_at=datetime.utcnow()
        )
        self.comments.append(comment)
        self.updated_at = datetime.utcnow()


class IncidentComment:
    """Комментарий к инциденту"""

    def __init__(self, text: str, user_id: UUID, created_at: datetime):
        self.text = text
        self.user_id = user_id
        self.created_at = created_at
