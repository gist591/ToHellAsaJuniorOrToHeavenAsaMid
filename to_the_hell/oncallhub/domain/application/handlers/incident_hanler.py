from typing import TYPE_CHECKING

from to_the_hell.oncallhub.api.schemas.incident import IncidentSchema
from to_the_hell.oncallhub.domain.commands.base import (
    Command,
    CommandHandler,
    CommandResult,
)
from to_the_hell.oncallhub.domain.commands.incident_commands import (
    GetAllIncidentsCommand,
)
from to_the_hell.oncallhub.domain.repositories import BaseIncidentRepository
from to_the_hell.oncallhub.domain.value_objects.incident_priority import (
    IncidentPriority,
)

if TYPE_CHECKING:
    pass


class GetAllIncidentsHandler(CommandHandler[list[IncidentSchema]]):
    def __init__(self, repository: BaseIncidentRepository):
        self.repository = repository

    async def handle(self, command: Command) -> CommandResult[list[IncidentSchema]]:
        if not isinstance(command, GetAllIncidentsCommand):
            return CommandResult.failure("Invalid command type")

        try:
            incidents = await self.repository.get_all_incidents(
                limit=command.limit,
                offset=command.offset,
                status=command.status,
                assigned_to=command.assigned_to,
            )

            if not incidents:
                return CommandResult.success([])

            incident_schemas = [
                IncidentSchema(
                    id=incident.id,
                    description=incident.description,
                    incident_created_at=incident.created_at.timestamp(),
                    incident_assigned_at=incident.assigned_at.timestamp()
                    if incident.assigned_at
                    else None,
                    status=incident.status,
                    priority=IncidentPriority(incident.priority.value),
                    assigned_duty=incident.incident_duties,
                )
                for incident in incidents
                if incident.id
            ]

            return CommandResult.success(incident_schemas)

        except Exception as e:
            return CommandResult.failure(f"Failed to get incidents: {e!s}")

    def can_handle(self, command: Command) -> bool:
        return isinstance(command, GetAllIncidentsCommand)
