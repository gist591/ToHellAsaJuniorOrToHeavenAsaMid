from dataclasses import dataclass
from datetime import datetime

from to_the_hell.oncallhub.domain.commands.base import Command


@dataclass
class CreateDutyCommand(Command):
    """
    Command to create a new duty
    """

    id: int
    devops_id: int
    start_time: datetime
    end_time: datetime

    def get_command_type(self) -> str:
        """Get command type identifier"""
        return "create_duty"


@dataclass
class GetCurrentDutyCommand(Command):
    """
    Command to get current active duty
    """

    def get_command_type(self) -> str:
        """Get command type identifier"""
        return "get_current_duty"


@dataclass
class GetAllDutiesCommand(Command):
    """
    Command to get all duties with pagination
    """

    limit: int | None = None
    offset: int | None = None

    def get_command_type(self) -> str:
        """Get command type identifier"""
        return "get_all_duties"
