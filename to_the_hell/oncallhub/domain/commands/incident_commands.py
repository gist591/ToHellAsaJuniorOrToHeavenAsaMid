from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from to_the_hell.oncallhub.domain.commands.base import Command


@dataclass
class GetAllIncidentsCommand(Command):
    limit: Optional[int] = None
    offset: Optional[None] = None
    status: Optional[str] = None
    assigned_to: Optional[UUID] = None

    def get_command_type(self) -> str:
        return "get_all_incidents"
