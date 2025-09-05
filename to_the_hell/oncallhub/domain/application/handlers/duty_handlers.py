# to_the_hell/oncallhub/application/handlers/duty_handlers.py
from datetime import UTC, datetime
from uuid import uuid4
from typing import Optional, TYPE_CHECKING

from to_the_hell.oncallhub.domain.commands import (
    CommandHandler, 
    CommandResult, 
)
from to_the_hell.oncallhub.domain.commands.base import Command
from to_the_hell.oncallhub.domain.commands.duty_commands import (
    CreateDutyCommand,
    GetAllDutiesCommand,
    GetCurrentDutyCommand,
)
from to_the_hell.oncallhub.domain.entities import Duty
from to_the_hell.oncallhub.domain.repositories import BaseDutyRepository
from to_the_hell.oncallhub.api.schemas import DutySchema

if TYPE_CHECKING:
    from to_the_hell.oncallhub.api.schemas import DutySchema


class CreateDutyHandler(CommandHandler[DutySchema]):
    def __init__(self, repository: BaseDutyRepository):
        self.repository = repository
    
    async def handle(self, command: CreateDutyCommand) -> CommandResult[DutySchema]:
        if command.end_time <= command.start_time:
            return CommandResult.validation_error({
                "time_range": ["End time must be after start time"]
            })
        
        # overlapping = await self.repository.check_overlapping(...)
        
        try:
            duty = Duty(
                id=uuid4(),
                devops_id=command.devops_id,
                start_time=command.start_time,
                end_time=command.end_time,
                status=True,
                created_at=datetime.now(tz=UTC)
            )
            
            created_duty = await self.repository.create(duty)
            
            duty_schema = DutySchema(
                id=created_duty.id,
                devops_id=created_duty.devops_id,
                start_time=created_duty.start_time,
                end_time=created_duty.end_time,
                status=created_duty.status,
                created_at=created_duty.created_at
            )
            
            return CommandResult.success(duty_schema)
            
        except Exception as e:
            return CommandResult.failure(f"Failed to create duty: {str(e)}")
    
    def can_handle(self, command: Command) -> bool:
        return isinstance(command, CreateDutyCommand)


class GetCurrentDutyHandler(CommandHandler[Optional[DutySchema]]):
    def __init__(self, repository: BaseDutyRepository):
        self.repository = repository
    
    async def handle(self, command: GetCurrentDutyCommand) -> CommandResult[Optional[DutySchema]]:
        try:
            duty = await self.repository.get_current_duty()
            
            if not duty:
                return CommandResult.success(None)
            
            duty_schema = DutySchema(
                id=duty.id,
                devops_id=duty.devops_id,
                start_time=duty.start_time,
                end_time=duty.end_time,
                status=duty.status,
                created_at=duty.created_at
            )
            
            return CommandResult.success(duty_schema)
            
        except Exception as e:
            return CommandResult.failure(f"Failed to get current duty: {str(e)}")
    
    def can_handle(self, command: Command) -> bool:
        return isinstance(command, GetCurrentDutyCommand)



class GetAllDutiesHandler(CommandHandler[list[DutySchema]]):
    def __init__(self, repository: BaseDutyRepository):
        self.repository = repository
    
    async def handle(self, command: GetAllDutiesCommand) -> CommandResult[list[DutySchema]]:
        try:
            duties = await self.repository.get_all_duties(command.limit, command.offset)
            
            return CommandResult.success(duties)
            
        except Exception as e:
            return CommandResult.failure(f"Failed to get all duties: {str(e)}")
    
    def can_handle(self, command: Command) -> bool:
        return isinstance(command, GetAllDutiesCommand)