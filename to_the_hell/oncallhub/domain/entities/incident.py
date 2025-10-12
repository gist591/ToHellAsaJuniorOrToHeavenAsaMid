from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

from to_the_hell.oncallhub.domain.value_objects import DevopsId, IncidentPriority

if TYPE_CHECKING:
    from .incident_states import IncidentState


class Incident:
    """Domain entity for incident"""

    def __init__(
        self,
        id: UUID,
        title: str,
        description: str,
        priority: "IncidentPriority",
    ):
        self.title: str = title
        self.description: str = description
        self.priority: IncidentPriority = priority
        self.created_at: datetime = datetime.now(tz=UTC)

        from .incident_states import NewIncidentState

        self._state: IncidentState = NewIncidentState()

        self.id: UUID | None = None
        self.assigned_id: UUID | None = None
        self.assigned_at: datetime | None = None
        self.updated_at: datetime | None = None
        self.comments: list[IncidentComment] = []

        self.assigned_to: DevopsId | None = None
        self.started_work_at: datetime | None = None
        self.resolved_at: datetime | None = None
        self.closed_at: datetime | None = None

        self.incident_assigned: Any | None = None
        self.incident_duties: list[Any] | None = None

    def assign_to_devops(self, devops_id: DevopsId) -> None:
        """Assign incident to devops user"""
        self.assigned_id = devops_id.value
        self.assigned_to = devops_id
        self.assigned_at = datetime.now(tz=UTC)
        self.updated_at = datetime.now(tz=UTC)

    def add_comment(self, text: str, user_id: UUID) -> None:
        """Add comment to incident"""
        comment = IncidentComment(
            text=text, user_id=user_id, created_at=datetime.now(tz=UTC)
        )
        self.comments.append(comment)
        self.updated_at = datetime.now(tz=UTC)

    def set_state(self, state: "IncidentState") -> None:
        """Set new state for incident"""
        self._state = state
        self.updated_at = datetime.now(tz=UTC)

    def get_state(self) -> "IncidentState":
        """Get current state of incident"""
        return self._state

    def is_active(self) -> bool:
        """Check if incident is active"""
        from .incident_states import ClosedIncidentState, ResolvedIncidentState

        return not isinstance(
            self._state, (ClosedIncidentState | ResolvedIncidentState)
        )

    @property
    def status(self) -> str:
        """Get current status of incident"""
        return self._state.get_status().value


class IncidentComment:
    """Comment for incident"""

    def __init__(self, text: str, user_id: UUID, created_at: datetime):
        self.text = text
        self.user_id = user_id
        self.created_at = created_at
