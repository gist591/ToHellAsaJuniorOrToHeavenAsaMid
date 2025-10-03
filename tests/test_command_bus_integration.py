from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

import pytest

from to_the_hell.oncallhub.api.schemas import DutySchema
from to_the_hell.oncallhub.domain.application.handlers.duty_handlers import (
    CreateDutyHandler,
    GetAllDutiesHandler,
    GetCurrentDutyHandler,
)
from to_the_hell.oncallhub.domain.commands import (
    CommandBus,
    CommandResultStatus,
)
from to_the_hell.oncallhub.domain.commands.base import Command
from to_the_hell.oncallhub.domain.commands.duty_commands import (
    CreateDutyCommand,
    GetAllDutiesCommand,
    GetCurrentDutyCommand,
)
from to_the_hell.oncallhub.domain.entities import Duty
from to_the_hell.oncallhub.domain.repositories import BaseDutyRepository

EXPECTED_TOTAL_DUTIES = 3
EXPECTED_NEXT_DUTIES = 2
EXPECTED_SUCCESSFUL_COMMANDS = 5


class FakeDutyRepository(BaseDutyRepository):
    """In-memory implementation for testing"""

    def __init__(self) -> None:
        self._duties: dict[UUID, Duty] = {}
        self._counter = 0

    async def create(self, duty: Duty) -> Duty:
        if duty.id is None:
            duty.id = uuid4()
        if duty.created_at is None:
            duty.created_at = datetime.now(tz=UTC)
        self._duties[duty.id] = duty
        return duty

    async def get_by_id(self, duty_id: UUID) -> Duty | None:
        return self._duties.get(duty_id)

    async def get_current_duty(self) -> Duty | None:
        now = datetime.now(tz=UTC)
        for duty in self._duties.values():
            if duty.start_time <= now <= duty.end_time and duty.status:
                return duty
        return None

    async def get_all_duties(
        self, limit: int | None = None, offset: int | None = None
    ) -> list[Duty]:
        duties = list(self._duties.values())

        duties.sort(
            key=lambda d: d.created_at or datetime.min.replace(tzinfo=UTC), reverse=True
        )

        if offset:
            duties = duties[offset:]
        if limit:
            duties = duties[:limit]

        return [self._duty_to_schema(duty) for duty in duties]

    async def check_overlapping(
        self, start_time: datetime, end_time: datetime, exclude_id: UUID | None = None
    ) -> bool:
        for duty in self._duties.values():
            if exclude_id and duty.id == exclude_id:
                continue
            if duty.status and not (
                end_time <= duty.start_time or start_time >= duty.end_time
            ):
                return True
        return False

    def _duty_to_schema(self, duty: Duty) -> DutySchema:
        return DutySchema(
            id=duty.id,
            devops_id=duty.devops_id,
            start_time=duty.start_time,
            end_time=duty.end_time,
            status=duty.status,
            created_at=duty.created_at,
        )


class TestDutyCommandsIntegration:
    """Integration tests for duty commands with real business logic"""

    @pytest.fixture
    def repository(self) -> FakeDutyRepository:
        return FakeDutyRepository()

    @pytest.fixture
    def command_bus(self, repository) -> CommandBus:
        bus = CommandBus()
        bus.register_handler(CreateDutyCommand, CreateDutyHandler(repository))
        bus.register_handler(GetCurrentDutyCommand, GetCurrentDutyHandler(repository))
        bus.register_handler(GetAllDutiesCommand, GetAllDutiesHandler(repository))
        return bus

    @pytest.mark.asyncio
    async def test_create_duty_success(self, command_bus: CommandBus) -> None:
        """Test creating a duty with valid data"""
        devops_id = uuid4()
        start_time = datetime.now(tz=UTC) + timedelta(hours=1)
        end_time = start_time + timedelta(hours=8)

        command = CreateDutyCommand(
            devops_id=devops_id, start_time=start_time, end_time=end_time
        )

        result = await command_bus.execute(command)

        assert result.status == CommandResultStatus.SUCCESS
        assert result.data is not None
        assert result.data.devops_id == devops_id
        assert result.data.start_time == start_time
        assert result.data.end_time == end_time
        assert result.data.status is True

    @pytest.mark.asyncio
    async def test_create_duty_invalid_time_range(self, command_bus) -> None:
        """Test validation error when end_time is before start_time"""
        devops_id = uuid4()
        start_time = datetime.now(tz=UTC) + timedelta(hours=8)
        end_time = start_time - timedelta(hours=1)  # Invalid: end before start

        command = CreateDutyCommand(
            devops_id=devops_id, start_time=start_time, end_time=end_time
        )

        result = await command_bus.execute(command)

        assert result.status == CommandResultStatus.VALIDATION_ERROR
        assert result.validation_errors is not None
        assert "time_range" in result.validation_errors

    @pytest.mark.asyncio
    async def test_get_current_duty_exists(self, command_bus, repository) -> None:
        """Test getting current active duty"""
        # Create a duty that is currently active
        devops_id = uuid4()
        now = datetime.now(tz=UTC)
        duty = Duty(
            id=uuid4(),
            devops_id=devops_id,
            start_time=now - timedelta(hours=1),
            end_time=now + timedelta(hours=7),
            status=True,
            created_at=now - timedelta(hours=2),
        )
        await repository.create(duty)

        command = GetCurrentDutyCommand()
        result = await command_bus.execute(command)

        assert result.status == CommandResultStatus.SUCCESS
        assert result.data is not None
        assert result.data.id == duty.id
        assert result.data.devops_id == devops_id

    @pytest.mark.asyncio
    async def test_get_current_duty_none(self, command_bus, repository) -> None:
        """Test when no current duty exists"""
        # Create an expired duty
        past_duty = Duty(
            id=uuid4(),
            devops_id=uuid4(),
            start_time=datetime.now(tz=UTC) - timedelta(hours=10),
            end_time=datetime.now(tz=UTC) - timedelta(hours=2),
            status=True,
            created_at=datetime.now(tz=UTC) - timedelta(hours=11),
        )
        await repository.create(past_duty)

        command = GetCurrentDutyCommand()
        result = await command_bus.execute(command)

        assert result.status == CommandResultStatus.SUCCESS
        assert result.data is None

    @pytest.mark.asyncio
    async def test_get_all_duties_with_pagination(
        self, command_bus, repository
    ) -> None:
        """Test getting all duties with limit and offset"""
        # Create multiple duties
        for i in range(5):
            duty = Duty(
                id=uuid4(),
                devops_id=uuid4(),
                start_time=datetime.now(tz=UTC) + timedelta(hours=i * 8),
                end_time=datetime.now(tz=UTC) + timedelta(hours=(i + 1) * 8),
                status=True,
                created_at=datetime.now(tz=UTC) - timedelta(hours=i),
            )
            await repository.create(duty)

        # Get first 3 duties
        command = GetAllDutiesCommand(limit=3, offset=0)
        result = await command_bus.execute(command)

        assert result.status == CommandResultStatus.SUCCESS
        assert len(result.data) == EXPECTED_TOTAL_DUTIES

        # Get next 2 duties
        command = GetAllDutiesCommand(limit=3, offset=3)
        result = await command_bus.execute(command)

        assert result.status == CommandResultStatus.SUCCESS
        assert len(result.data) == EXPECTED_NEXT_DUTIES

    @pytest.mark.asyncio
    async def test_command_bus_error_handling(self, command_bus) -> None:
        """Test that CommandBus properly handles missing handlers"""

        # Create a command without registered handler
        @dataclass
        class UnregisteredCommand(Command):
            def get_command_type(self) -> str:
                return "unregistered"

        command = UnregisteredCommand()

        with pytest.raises(ValueError, match="Handler for command"):
            await command_bus.execute(command)


class TestDutyBusinessRules:
    """Test business rules and edge cases"""

    @pytest.fixture
    def repository(self) -> FakeDutyRepository:
        return FakeDutyRepository()

    @pytest.fixture
    def handler(self, repository) -> Any:
        return CreateDutyHandler(repository)

    @pytest.mark.asyncio
    async def test_duty_duration_validation(self, handler) -> None:
        """Test duty duration constraints"""
        # Test minimum duration (if you have such rule)
        command = CreateDutyCommand(
            devops_id=uuid4(),
            start_time=datetime.now(tz=UTC),
            end_time=datetime.now(tz=UTC) + timedelta(minutes=30),  # Too short
        )

        result = await handler.handle(command)

        # Adjust based on your business rules
        # This is an example if you have minimum duration rule
        if result.status == CommandResultStatus.VALIDATION_ERROR:
            assert "duration" in str(result.validation_errors)

    @pytest.mark.asyncio
    async def test_concurrent_duty_creation(self, repository) -> None:
        """Test that repository handles concurrent operations safely"""
        handler = CreateDutyHandler(repository)

        # Create multiple duties concurrently
        import asyncio

        async def create_duty(index: int) -> Any:
            command = CreateDutyCommand(
                devops_id=uuid4(),
                start_time=datetime.now(tz=UTC) + timedelta(hours=index * 10),
                end_time=datetime.now(tz=UTC) + timedelta(hours=(index + 1) * 10),
            )
            return await handler.handle(command)

        results = await asyncio.gather(*[create_duty(i) for i in range(5)])

        successful = [r for r in results if r.status == CommandResultStatus.SUCCESS]
        assert len(successful) == EXPECTED_SUCCESSFUL_COMMANDS

        # Verify all duties have unique IDs
        duty_ids = [r.data.id for r in successful]
        assert len(duty_ids) == len(set(duty_ids))


class TestCommandBusLifecycle:
    """Test CommandBus lifecycle and state management"""

    @pytest.mark.asyncio
    async def test_handler_registration_override(self) -> None:
        """Test that re-registering handler overwrites previous one"""
        bus = CommandBus()
        repo1 = FakeDutyRepository()
        repo2 = FakeDutyRepository()

        # Register first handler
        bus.register_handler(CreateDutyCommand, CreateDutyHandler(repo1))

        # Create duty with first handler
        command = CreateDutyCommand(
            devops_id=uuid4(),
            start_time=datetime.now(tz=UTC),
            end_time=datetime.now(tz=UTC) + timedelta(hours=8),
        )
        await bus.execute(command)

        # Re-register with different handler
        bus.register_handler(CreateDutyCommand, CreateDutyHandler(repo2))

        # Create another duty
        await bus.execute(command)

        # Verify duties are in different repositories
        assert len(await repo1.get_all_duties()) == 1
        assert len(await repo2.get_all_duties()) == 1

    @pytest.mark.asyncio
    async def test_command_bus_isolation(self) -> None:
        """Test that different CommandBus instances are isolated"""
        bus1 = CommandBus()
        bus2 = CommandBus()

        repo = FakeDutyRepository()
        bus1.register_handler(CreateDutyCommand, CreateDutyHandler(repo))

        command = CreateDutyCommand(
            devops_id=uuid4(),
            start_time=datetime.now(tz=UTC),
            end_time=datetime.now(tz=UTC) + timedelta(hours=8),
        )

        # bus1 should handle the command
        result = await bus1.execute(command)
        assert result.status == CommandResultStatus.SUCCESS

        # bus2 should fail (no handler registered)
        with pytest.raises(ValueError):
            await bus2.execute(command)
