from typing import TYPE_CHECKING, List
from to_the_hell.oncallhub.api.schemas.incident import IncidentSchema
from to_the_hell.oncallhub.domain.commands.base import Command, CommandHandler, CommandResult
from to_the_hell.oncallhub.domain.commands.incident_commands import GetAllIncidentsCommand

if TYPE_CHECKING:
    from to_the_hell.oncallhub.domain.repositories.base import BaseIncidentRepository


class GetAllIncidentsHandler(CommandHandler[List[IncidentSchema]]):
    def __init__(self, repository: BaseIncidentRepository):
        self.repository = repository
    
    async def handle(self, command: GetAllIncidentsCommand) -> CommandResult[List[IncidentSchema]]:
        try:
            incidents = await self.repository.get_all_incidents(
                limit=command.limit,
                offset=command.offset,
                status=command.status,
                assigned_to=command.assigned_to
            )
            
            if not incidents:
                return CommandResult.success([])
            
            incident_schemas = [
                IncidentSchema(
                    id=incident.id,
                    description=incident.description,
                    incident_created_at=incident.created_at.timestamp(),
                    incident_assigned_at=incident.assigned_at.timestamp() if incident.assigned_at else None,
                    status=incident.status,
                    priority=incident.priority.value,
                    assigned_duty=incident.assidnged_duty
                )
                for incident in incidents
            ]
            
            return CommandResult.success(incident_schemas)
            
        except Exception as e:
            return CommandResult.failure(f"Failed to get incidents: {str(e)}")
    
    def can_handle(self, command: Command) -> bool:
        return isinstance(command, GetAllIncidentsCommand)
