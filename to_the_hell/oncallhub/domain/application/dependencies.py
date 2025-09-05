from functools import lru_cache

from to_the_hell.oncallhub.application.handlers.duty_handlers import CreateDutyHandler, GetAllDutiesHandler, GetCurrentDutyHandler
from to_the_hell.oncallhub.domain.commands.base import CommandBus
from to_the_hell.oncallhub.domain.commands.duty_commands import CreateDutyCommand, GetAllDutiesCommand, GetCurrentDutyCommand
from to_the_hell.oncallhub.infra.db import PostgresDutyRepository
from sqlalchemy.ext.asyncio import AsyncSession


@lru_cache()
def get_command_bus(session: AsyncSession) -> CommandBus:
    '''Dependency for getting CommandBus'''
    command_bus = CommandBus()
    
    duty_repo = PostgresDutyRepository(session)

    command_bus.register_handler(CreateDutyCommand, CreateDutyHandler(duty_repo))
    command_bus.register_handler(GetCurrentDutyCommand, GetCurrentDutyHandler(duty_repo))
    command_bus.register_handler(GetAllDutiesCommand, GetAllDutiesHandler(duty_repo))

    return command_bus