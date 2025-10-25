from typing import Any, cast

from fastapi import APIRouter, Depends, HTTPException

from to_the_hell.oncallhub.api.deps import CommandBusDep, get_current_user
from to_the_hell.oncallhub.api.schemas import DutySchema
from to_the_hell.oncallhub.domain.commands import CommandResultStatus
from to_the_hell.oncallhub.domain.commands.duty_commands import (
    CreateDutyCommand,
    GetAllDutiesCommand,
    GetCurrentDutyCommand,
)

router = APIRouter()


@router.get("/duties", response_model=list[DutySchema])
async def get_all_duties(
    command_bus: CommandBusDep,
) -> list[DutySchema]:
    """Get all duties"""

    command = GetAllDutiesCommand()
    result = await command_bus.execute(command)

    if result.status == CommandResultStatus.FAILURE:
        raise HTTPException(status_code=500, detail=result.error_message)

    return cast(list[DutySchema], result.data) if result.data else []


@router.get("/current-duty/", response_model=DutySchema | None)
async def get_current_duty(
    command_bus: CommandBusDep,
) -> DutySchema | None:
    """Get current duty"""
    command = GetCurrentDutyCommand()
    result = await command_bus.execute(command)

    if result.status == CommandResultStatus.FAILURE:
        raise HTTPException(status_code=500, detail=result.error_message)

    return cast(DutySchema, result.data) if result.data else None


@router.post("/put-on-duty/", response_model=DutySchema)
async def create_duty(
    duty_data: DutySchema,
    command_bus: CommandBusDep,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> DutySchema:
    """Create new duty"""
    command = CreateDutyCommand(
        id=duty_data.id,
        devops_id=duty_data.devops_id,
        start_time=duty_data.start_time,
        end_time=duty_data.end_time,
    )

    result = await command_bus.execute(command)

    if result.status == CommandResultStatus.VALIDATION_ERROR:
        raise HTTPException(status_code=400, detail=result.validation_errors)

    if result.status == CommandResultStatus.FAILURE:
        raise HTTPException(status_code=500, detail=result.error_message)

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create duty")

    return cast(DutySchema, result.data)
