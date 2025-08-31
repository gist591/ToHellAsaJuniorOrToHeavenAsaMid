from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from to_the_hell.oncallhub.api.schemas import DutySchema
from to_the_hell.oncallhub.domain.entities import Duty
from to_the_hell.oncallhub.infra.db import PostgresDutyRepository, get_session
from to_the_hell.oncallhub.domain.value_objects import DutyId, TimeRange, UserId

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
        TimeRange(
            start=duty.time_range.start.timestamp(),
            end=duty.time_range.end.timestamp(),
        ),
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
            start=created_duty.time_range.start.timestamp(),
            end=created_duty.time_range.end.timestamp(),
        ),
        status=duty_data.status,
    )


@router.get('/duties') # type: ignore[misc]
def get_all_duties(
    session: AsyncSession = Depends(get_session)
) -> List[Duty]:
    """
    Get all duties in history

    Return:
        404: current duty is not exist
        200: current duty
    """

    repo = PostgresDutyRepository(session)
    duties = repo.get_all_duties()

    if not duties:
        raise HTTPException(status_code=404, detail="No duties found")

    dutie_schemas = [
        DutySchema(
            id=UUID(str(duty.id)),
            description=duty.description,
            dutie_created_at=duty.dutie_created,
            dutie_assigned_at=duty.duty.assigned,
            status=duty.status,
            priority=duty.priority,
            assigned_duty=duty.assigned_duty

        ) for duty in duties
    ]

    return dutie_schemas
