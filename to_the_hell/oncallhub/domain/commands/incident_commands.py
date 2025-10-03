from dataclasses import dataclass
from uuid import UUID

from to_the_hell.oncallhub.domain.commands.base import Command


@dataclass
class GetAllIncidentsCommand(Command):
    limit: int | None = None
    offset: int | None = None
    status: str | None = None
    assigned_to: UUID | None = None

    def get_command_type(self) -> str:
        return "get_all_incidents"
