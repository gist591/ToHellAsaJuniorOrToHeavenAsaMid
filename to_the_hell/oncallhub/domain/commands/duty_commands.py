from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from to_the_hell.oncallhub.domain.commands.base import (
    Command,
)

if TYPE_CHECKING:
    pass


@dataclass
class CreateDutyCommand(Command):
    devops_id: UUID
    start_time: datetime
    end_time: datetime

    def get_command_type(self) -> str:
        return "create_duty"


@dataclass
class GetCurrentDutyCommand(Command):
    def get_command_type(self) -> str:
        return "get_current_duty"


@dataclass
class GetAllDutiesCommand(Command):
    limit: int | None = None
    offset: int | None = None

    def get_command_type(self) -> str:
        return "get_all_duties"
