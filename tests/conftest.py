from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from random import randint

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from tests.fakes import (
    FakeDuty,
    FakeDutyRepository,
    FakeTelegramNotificationService,
    FakeUser,
    FakeUserRepository,
)
from to_the_hell.oncallhub.domain.entities import Devops
from to_the_hell.oncallhub.domain.repositories import BaseDevopsRepository

pytest_plugins = ["pytest_asyncio"]


class FakeDevopsRepostitory(BaseDevopsRepository):
    """
    Fake devops repository for tests
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, devops: Devops) -> Devops:
        return devops


FAKE_get_database_url = "sqlite+aiosqlite:///:memory:"

async_engine = create_async_engine(url=FAKE_get_database_url)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


@pytest_asyncio.fixture  # type: ignore[misc]
async def get_session() -> AsyncIterator[AsyncSession]:
    async_engine = create_async_engine(url=FAKE_get_database_url, echo=True)
    async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

    async with async_session_factory() as session:
        yield session

    await async_engine.dispose()


@pytest.fixture
def duty_repo():
    """Fixture: Clean duty repository for each test"""
    repo = FakeDutyRepository()
    yield repo
    repo.clear()


@pytest.fixture
def user_repo():
    """Fixture: Clean user repository for each test"""
    repo = FakeUserRepository()
    yield repo
    repo.clear()


@pytest.fixture
def notification_service():
    """Fixture: Clean notification service for each test"""
    service = FakeTelegramNotificationService()
    yield service
    service.clear()


@pytest.fixture
def sample_user(user_repo):
    """Fixture: Create sample user with Telegram"""
    user = FakeUser(
        id=randint(0, 10000),
        email="devops@example.com",
        full_name="John DevOps",
        telegram_chat_id="123456789",
    )
    user_repo.add(user)
    return user


@pytest.fixture
def sample_duty_in_24h(duty_repo, sample_user):
    """Fixture: Create duty starting in 24 hours"""
    now = datetime.now(UTC)
    duty = FakeDuty(
        id=randint(0, 10000),
        devops_id=sample_user.id,
        start_time=now + timedelta(hours=24),
        end_time=now + timedelta(hours=32),
        reminder_24h_sent=False,
        reminder_2h_sent=False,
        reminder_10m_sent=False,
    )
    duty_repo.add(duty)
    return duty


@pytest.fixture
def sample_duty_in_2h(duty_repo, sample_user):
    """Fixture: Create duty starting in 2 hours"""
    now = datetime.now(UTC)
    duty = FakeDuty(
        id=randint(0, 10000),
        devops_id=sample_user.id,
        start_time=now + timedelta(hours=2),
        end_time=now + timedelta(hours=10),
        reminder_24h_sent=True,  # 24h already sent
        reminder_2h_sent=False,
        reminder_10m_sent=False,
    )
    duty_repo.add(duty)
    return duty


@pytest.fixture
def sample_duty_in_10m(duty_repo, sample_user):
    """Fixture: Create duty starting in 10 minutes"""
    now = datetime.now(UTC)
    duty = FakeDuty(
        id=randint(0, 10000),
        devops_id=sample_user.id,
        start_time=now + timedelta(minutes=10),
        end_time=now + timedelta(hours=8),
        reminder_24h_sent=True,  # Previous reminders sent
        reminder_2h_sent=True,
        reminder_10m_sent=False,
    )
    duty_repo.add(duty)
    return duty
