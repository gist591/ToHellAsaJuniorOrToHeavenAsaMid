from typing import cast

from fastapi import APIRouter, Depends, HTTPException

from to_the_hell.oncallhub.api.schemas.incident import IncidentSchema
from to_the_hell.oncallhub.domain.application.dependencies import get_command_bus
from to_the_hell.oncallhub.domain.commands import (
    GetAllIncidentsCommand,
)
from to_the_hell.oncallhub.domain.commands.base import CommandBus, CommandResultStatus

router = APIRouter()


@router.get("/incidents", response_model=list[IncidentSchema])
async def get_all_incidents(
    limit: int = 100,
    offset: int = 0,
    status: str | None = None,
    command_bus: CommandBus = Depends(get_command_bus),
) -> list[IncidentSchema]:
    """
    Get all incidents in history
    """
    command = GetAllIncidentsCommand(limit=limit, offset=offset, status=status)

    result = await command_bus.execute(command)

    if result.status == CommandResultStatus.FAILURE:
        raise HTTPException(status_code=500, detail=result.error_message)

    return cast(list[IncidentSchema], result.data) if result.data else []
