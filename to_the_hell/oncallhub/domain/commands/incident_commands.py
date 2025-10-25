from dataclasses import dataclass

from to_the_hell.oncallhub.domain.commands.base import Command


@dataclass
class GetAllIncidentsCommand(Command):
    """
    Command to get all incidents with filtering
    """

    limit: int | None = None
    offset: int | None = None
    status: str | None = None
    assigned_to: int | None = None

    def get_command_type(self) -> str:
        """Get command type identifier"""
        return "get_all_incidents"
