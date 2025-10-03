# scripts/seed.py
import asyncio
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from to_the_hell.oncallhub.infra.db.models.devops import DevopsORM
from to_the_hell.oncallhub.infra.db.models.duty import DutyORM
from to_the_hell.oncallhub.infra.db.models.incident import IncidentORM
from to_the_hell.oncallhub.infra.db.session import async_session_factory


async def seed_devops(session: AsyncSession) -> list[int]:
    """Create test devops users"""
    devops_data = [
        {"name": "Иван Петров", "telegram_username": "@ivan_ops"},
        {"name": "Мария Сидорова", "telegram_username": "@maria_dev"},
        {"name": "Алексей Гречанов", "telegram_username": "@alex_sre"},
    ]

    devops_ids = []
    for data in devops_data:
        devops = DevopsORM(**data)
        session.add(devops)
        await session.flush()
        devops_ids.append(devops.id)

    await session.commit()
    print(f"Created {len(devops_data)} devops users")
    return devops_ids


async def seed_duties(session: AsyncSession, devops_ids: list[int]) -> None:
    """Create duty schedule for one week"""
    now = datetime.now(UTC).replace(hour=9, minute=0, second=0, microsecond=0)

    duties = []
    for i in range(7):
        duty = DutyORM(
            user_id=devops_ids[i % len(devops_ids)],
            start_time=now + timedelta(days=i),
            end_time=now + timedelta(days=i + 1),
            status=True,
        )
        duties.append(duty)

    session.add_all(duties)
    await session.commit()
    print(f"Created {len(duties)} duties")


async def seed_incidents(session: AsyncSession) -> None:
    """Create test incidents"""
    now = datetime.now(UTC)

    incidents_data = [
        {
            "description": "База данных недоступна на production",
            "incident_created": (now - timedelta(hours=2)).timestamp(),
            "status": "new",
            "priority": 4,  # critical
            "incident_assigned": None,
            "assigned_duty": None,
        },
        {
            "description": "Высокая нагрузка CPU на worker-01",
            "incident_created": (now - timedelta(days=1)).timestamp(),
            "incident_assigned": (now - timedelta(hours=23)).timestamp(),
            "status": "assigned",
            "priority": 3,  # high
            "assigned_duty": [],
        },
        {
            "description": "SSL сертификат истекает через 7 дней",
            "incident_created": (now - timedelta(days=3)).timestamp(),
            "incident_assigned": (now - timedelta(days=2)).timestamp(),
            "status": "resolved",
            "priority": 1,  # low
            "assigned_duty": [],
        },
    ]

    for data in incidents_data:
        incident = IncidentORM(**data)
        session.add(incident)

    await session.commit()
    print(f"Created {len(incidents_data)} incidents")


async def main() -> None:
    """Main seed function"""
    print("Starting seed script...")

    async with async_session_factory() as session:
        try:
            devops_ids = await seed_devops(session)
            await seed_duties(session, devops_ids)
            await seed_incidents(session)

            print("\nSeed completed successfully!")

        except Exception as e:
            print(f"❌ Error: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(main())
