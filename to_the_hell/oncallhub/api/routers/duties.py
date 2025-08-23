from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from to_the_hell.oncallhub.api.schemas import DutySchema
from to_the_hell.oncallhub.entitites import Duty
from to_the_hell.oncallhub.infra.db import PostgresDutyRepository, get_session
from to_the_hell.oncallhub.value_objects import DutyId, TimeRange, UserId

router = APIRouter()


@router.get("/current-duty/", response_model=DutySchema)  # type: ignore[misc]
async def get_current_duty(session: AsyncSession = Depends(get_session)) -> Any:
    """
    Get current duty

    Return:
        404: current duty is not exist
        200: current duty
    """

    repo = PostgresDutyRepository(session)
    duty = await repo.get_current_duty()
    if not duty:
        raise HTTPException(status_code=404, detail="No current duty found")
    return DutySchema(
        id=UUID(str(duty.id)),
        user_id=UUID(str(duty.user_id)),
        start_time=duty.time_range.start.timestamp(),
        end_time=duty.time_range.end.timestamp(),
        status=duty.status,
    )


@router.post("/put-on-duty/", response_model=DutySchema)  # type: ignore[misc]
async def create_duty(
    duty_data: Duty, session: AsyncSession = Depends(get_session)
) -> Duty:
    """
    Create new duty

    TODO: Check that there are no overkaps,
    user rights check,
    validating time range
    """

    repo = PostgresDutyRepository(session)
    duty = Duty(
        id=DutyId.generate(),
        user_id=UserId.from_string(str(duty_data.user_id)),
        time_range=TimeRange(
            start=datetime.fromtimestamp(duty_data.start_time, tz=UTC),
            end=datetime.fromtimestamp(duty_data.end_time, tz=UTC),
        ),
        status=duty_data.status,
    )

    created_duty = await repo.create(duty)

    return DutySchema(
        id=UUID(str(created_duty.id)),
        user_id=UserId.from_string(str(duty_data.user_id)),
        time_range=TimeRange(
            start_time=created_duty.time_range.start.timestamp(),
            end_time=created_duty.time_range.end.timestamp(),
        ),
        status=duty_data.status,
    )
