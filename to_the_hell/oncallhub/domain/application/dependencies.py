from sqlalchemy.ext.asyncio import AsyncSession

from to_the_hell.oncallhub.domain.application.handlers import (
    CreateDutyHandler,
    GetAllDutiesHandler,
    GetCurrentDutyHandler,
)
from to_the_hell.oncallhub.domain.commands.base import CommandBus
from to_the_hell.oncallhub.domain.commands.duty_commands import (
    CreateDutyCommand,
    GetAllDutiesCommand,
    GetCurrentDutyCommand,
)
from to_the_hell.oncallhub.infra.db.repositories import PostgresDutyRepository


async def get_command_bus(session: AsyncSession) -> CommandBus:
    """
    Create and configure Command Bus with all handlers
    for get_commands_bus_dependency

    Do not use this directly with FastAPI Depends()!
    """
    command_bus = CommandBus()

    duty_repo = PostgresDutyRepository(session)

    command_bus.register_handler(CreateDutyCommand, CreateDutyHandler(duty_repo))
    command_bus.register_handler(
        GetCurrentDutyCommand, GetCurrentDutyHandler(duty_repo)
    )
    command_bus.register_handler(GetAllDutiesCommand, GetAllDutiesHandler(duty_repo))

    return command_bus
