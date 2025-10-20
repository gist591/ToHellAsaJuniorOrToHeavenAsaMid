from typing import cast

from fastapi import APIRouter, HTTPException

from to_the_hell.oncallhub.api.deps import CommandBusDep
from to_the_hell.oncallhub.api.schemas.incident import IncidentSchema
from to_the_hell.oncallhub.domain.commands import (
    CommandResultStatus,
    GetAllIncidentsCommand,
)

router = APIRouter()


@router.get("/incidents", response_model=list[IncidentSchema])
async def get_all_incidents(
    command_bus: CommandBusDep,
    limit: int = 100,
    offset: int = 0,
    status: str | None = None,
) -> list[IncidentSchema]:
    """
    Get all incidents in history
    """
    command = GetAllIncidentsCommand(limit=limit, offset=offset, status=status)

    result = await command_bus.execute(command)

    if result.status == CommandResultStatus.FAILURE:
        raise HTTPException(status_code=500, detail=result.error_message)

    return cast(list[IncidentSchema], result.data) if result.data else []
