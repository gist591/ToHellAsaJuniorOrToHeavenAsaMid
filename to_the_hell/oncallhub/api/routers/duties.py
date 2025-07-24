from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from to_the_hell.oncallhub.api.schemas import Duty
from to_the_hell.oncallhub.infra.db import PostgresDutyRepository, get_session


router = APIRouter()

@router.get('/current-duty/')
async def get_current_duty(session: AsyncSession = Depends(get_session)) -> Duty:
    """
    Получить Duty, который на данный момент на смене
    """

    repo = PostgresDutyRepository(session)
    duty = await repo.get_current_duty()
    if not duty:
        raise HTTPException(status_code=404, detail="No current duty found")
    return Duty.model_validate(duty)


@router.post('/put-on-duty/')
async def put_on_duty(duty_data: Duty, session:
    AsyncSession = Depends(get_session)) -> Duty:
    """
    Добавить в дежурства работника
    """

    repo = PostgresDutyRepository(session)
    duty = await repo.create(**duty_data.model_dump())
    return Duty.model_validate(duty)
