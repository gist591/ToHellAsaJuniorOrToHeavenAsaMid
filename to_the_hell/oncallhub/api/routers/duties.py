from fastapi import APIRouter, Depends, HTTPException

from to_the_hell.oncallhub.api.schemas import DutySchema
from to_the_hell.oncallhub.domain.application.dependencies import (
    get_command_bus,
)
from to_the_hell.oncallhub.domain.commands import CommandBus, CommandResultStatus
from to_the_hell.oncallhub.domain.commands.duty_commands import (
    CreateDutyCommand,
    GetAllDutiesCommand,
    GetCurrentDutyCommand,
)


router = APIRouter()


@router.get("/current-duty/", response_model=DutySchema | None)  # type: ignore[misc]
async def get_current_duty(
    command_bus: CommandBus = Depends(get_command_bus),
) -> DutySchema:
    command = GetCurrentDutyCommand()
    result = await command_bus.execute(command)

    if result.status == CommandResultStatus.FAILURE:
        raise HTTPException(status_code=500, detail=result.error_message)

    if result.data is None:
        raise HTTPException(status_code=404, detail="No current duty found")

    return result.data


@router.post("/put-on-duty/", response_model=DutySchema)  # type: ignore[misc]
async def create_duty(
    duty_data: DutySchema, command_bus: CommandBus = Depends(get_command_bus)
) -> DutySchema:
    command = CreateDutyCommand(
        devops_id=duty_data.devops_id,
        start_time=duty_data.start_time,
        end_time=duty_data.end_time,
    )

    result = await command_bus.execute(command)

    if result.status == CommandResultStatus.VALIDATION_ERROR:
        raise HTTPException(status_code=400, detail=result.validation_errors)

    if result.status == CommandResultStatus.FAILURE:
        raise HTTPException(status_code=500, detail=result.error_message)

    return result.data


@router.get("/duties", response_model=list[DutySchema])  # type: ignore[misc]
async def get_all_duties(
    command_bus: CommandBus = Depends(get_command_bus),
) -> list[DutySchema]:
    command = GetAllDutiesCommand()
    result = await command_bus.execute(command)

    return result.data
