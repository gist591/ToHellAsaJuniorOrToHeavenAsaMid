from dataclasses import dataclass, field
from typing import Any, Protocol
from unittest.mock import AsyncMock

import pytest

from to_the_hell.oncallhub.domain.commands import (
    Command,
    CommandBus,
    CommandHandler,
    CommandResult,
    CommandResultStatus,
)


class CommandFactory(Protocol):
    """Protocol for command factory"""

    def create_command(self, **kwargs: Any) -> Command: ...


class TestHandler(CommandHandler[dict[str, Any]]):
    """Test handler with additional attributes for assertions"""

    handle_called: bool
    last_command: Command | None
    call_count: int

    def __init__(self) -> None:
        self.handle_called = False
        self.last_command = None
        self.call_count = 0

    async def handle(self, command: Command) -> CommandResult[dict[str, Any]]:
        self.handle_called = True
        self.last_command = command
        self.call_count += 1
        return CommandResult.success(
            {
                "test": "data",
                "command_type": command.get_command_type(),
                "call_count": self.call_count,
            }
        )

    def can_handle(self, command: Command) -> bool:
        return True


@pytest.fixture  # type: ignore[misc]
def command_bus() -> CommandBus:
    """Create command bus instance"""
    return CommandBus()


@pytest.fixture  # type: ignore[misc]
def command_factory() -> CommandFactory:
    """Factory for creating test commands"""

    class Factory:
        def create_command(self, **kwargs: Any) -> Command:
            @dataclass
            class DynamicCommand(Command):
                data: dict[str, Any] = field(default_factory=lambda: kwargs)

                def get_command_type(self) -> str:
                    return f"dynamic_{id(self)}"

            return DynamicCommand()

    return Factory()


@pytest.fixture  # type: ignore[misc]
def test_command_class() -> type[Command]:
    """Create test command class"""

    @dataclass
    class TestCommand(Command):
        payload: dict[str, Any] = field(default_factory=dict)

        def get_command_type(self) -> str:
            return "test_command"

    return TestCommand


@pytest.fixture  # type: ignore[misc]
def test_handler_class(
    test_command_class: type[Command],
) -> type[TestHandler]:
    """Create test handler class"""

    class TestHandlerImpl(TestHandler):
        def __init__(self) -> None:
            super().__init__()
            self._command_class = test_command_class

        def can_handle(self, command: Command) -> bool:
            return isinstance(command, self._command_class)

    return TestHandlerImpl


class TestCommandResult:
    """Test CommandResult functionality"""

    @pytest.mark.parametrize(  # type: ignore[misc]
        "data,expected",
        [
            ({"id": 1, "name": "test"}, {"id": 1, "name": "test"}),
            ({}, {}),
            (None, None),
            ({"nested": {"key": "value"}}, {"nested": {"key": "value"}}),
            ([], []),
        ],
    )
    def test_success_creation(self, data: Any, expected: Any) -> None:
        """Test successful command result creation with various data types"""
        result: CommandResult[Any] = CommandResult.success(data)

        assert result.status == CommandResultStatus.SUCCESS
        assert result.data == expected
        assert result.error_message is None
        assert result.validation_errors is None

    @pytest.mark.parametrize(  # type: ignore[misc]
        "error_msg",
        [
            "Something went wrong",
            "",
            "Database connection failed",
            "Timeout occurred",
            "Service unavailable",
        ],
    )
    def test_failure_creation(self, error_msg: str) -> None:
        """Test failure command result creation with various messages"""
        result: CommandResult[Any] = CommandResult.failure(error_msg)

        assert result.status == CommandResultStatus.FAILURE
        assert result.data is None
        assert result.error_message == error_msg
        assert result.validation_errors is None

    @pytest.mark.parametrize(  # type: ignore[misc]
        "validation_errors",
        [
            {"title": ["Title is required"]},
            {"email": ["Invalid format"], "phone": ["Too short"]},
            {},
            {"nested": ["Error 1", "Error 2", "Error 3"]},
        ],
    )
    def test_validation_error_creation(
        self, validation_errors: dict[str, list[str]]
    ) -> None:
        """Test validation error command result creation"""
        result: CommandResult[Any] = CommandResult.validation_error(validation_errors)

        assert result.status == CommandResultStatus.VALIDATION_ERROR
        assert result.data is None
        assert result.error_message is None
        assert result.validation_errors == validation_errors


class TestCommandResultStatus:
    """Test CommandResultStatus enum"""

    def test_enum_values(self) -> None:
        """Test command result status enum values"""
        assert CommandResultStatus.SUCCESS.value == "success"
        assert CommandResultStatus.FAILURE.value == "failure"
        assert CommandResultStatus.VALIDATION_ERROR.value == "validation_error"

    def test_enum_uniqueness(self) -> None:
        """Test that all enum values are unique"""
        values = [status.value for status in CommandResultStatus]
        assert len(values) == len(set(values))


class TestAbstractClasses:
    """Test abstract base classes behavior"""

    def test_command_cannot_be_instantiated(self) -> None:
        """Test that Command is an abstract base class"""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            Command()  # type: ignore[abstract]

    def test_command_handler_cannot_be_instantiated(self) -> None:
        """Test that CommandHandler is an abstract base class"""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            CommandHandler()  # type: ignore[abstract]


class TestCommandBus:
    """Test CommandBus functionality"""

    def test_initialization(self, command_bus: CommandBus) -> None:
        """Test command bus initialization"""
        assert isinstance(command_bus, CommandBus)

    def test_register_and_execute_flow(
        self,
        command_bus: CommandBus,
        test_command_class: type[Command],
        test_handler_class: type[TestHandler],
    ) -> None:
        """Test complete registration flow"""
        handler = test_handler_class()
        command_bus.register_handler(test_command_class, handler)
        assert not handler.handle_called
        assert handler.call_count == 0

    @pytest.mark.asyncio  # type: ignore[misc]
    async def test_successful_execution(
        self,
        command_bus: CommandBus,
        test_command_class: type[Command],
        test_handler_class: type[TestHandler],
    ) -> None:
        """Test successful command execution"""
        handler = test_handler_class()

        @dataclass
        class TestCommandWithPayload(Command):
            payload: dict[str, Any] = field(default_factory=dict)

            def get_command_type(self) -> str:
                return "test_command"

        command = TestCommandWithPayload(payload={"test": "value"})

        command_bus.register_handler(TestCommandWithPayload, handler)
        result = await command_bus.execute(command)

        assert result.status == CommandResultStatus.SUCCESS
        assert result.data is not None
        assert result.data["test"] == "data"
        assert handler.handle_called is True
        assert handler.last_command == command
        assert handler.call_count == 1

    @pytest.mark.asyncio  # type: ignore[misc]
    async def test_handler_not_found(
        self, command_bus: CommandBus, test_command_class: type[Command]
    ) -> None:
        """Test error when handler not found"""
        command = test_command_class()

        with pytest.raises(ValueError) as exc_info:
            await command_bus.execute(command)

        assert "Handler for command" in str(exc_info.value)

    @pytest.mark.asyncio  # type: ignore[misc]
    @pytest.mark.parametrize(  # type: ignore[misc]
        "handler_configs",
        [
            [{"id": 1, "result": {"handler": 1}}, {"id": 2, "result": {"handler": 2}}],
            [
                {"id": "A", "result": {"type": "A"}},
                {"id": "B", "result": {"type": "B"}},
            ],
        ],
    )
    async def test_multiple_handlers(
        self, command_bus: CommandBus, handler_configs: list[dict[str, Any]]
    ) -> None:
        """Test bus with multiple command handlers using parametrization"""
        commands: list[Command] = []
        handlers: list[AsyncMock] = []

        for config in handler_configs:

            @dataclass
            class DynamicCommand(Command):
                command_id: Any = config["id"]

                def get_command_type(self) -> str:
                    return f"command_{self.command_id}"

            handler = AsyncMock(return_value=CommandResult.success(config["result"]))
            command = DynamicCommand()

            commands.append(command)
            handlers.append(handler)
            command_bus.register_handler(type(command), handler)

        results: list[CommandResult[Any]] = []
        for command, handler in zip(commands, handlers, strict=False):
            result = await command_bus.execute(command)
            results.append(result)
            handler.handle.assert_called_once_with(command)

        for result, config in zip(results, handler_configs, strict=False):
            assert result.status == CommandResultStatus.SUCCESS
            assert result.data == config["result"]

    @pytest.mark.asyncio  # type: ignore[misc]
    async def test_handler_exception_propagation(
        self, command_bus: CommandBus, test_command_class: type[Command]
    ) -> None:
        """Test that handler exceptions are propagated"""

        class FailingHandler(CommandHandler[dict[str, Any]]):
            async def handle(self, command: Command) -> CommandResult[dict[str, Any]]:
                raise RuntimeError("Handler failed")

            def can_handle(self, command: Command) -> bool:
                return True

        command_bus.register_handler(test_command_class, FailingHandler())

        with pytest.raises(RuntimeError, match="Handler failed"):
            await command_bus.execute(test_command_class())


class TestIntegrationScenarios:
    """Integration tests for command pattern"""

    @pytest.mark.asyncio  # type: ignore[misc]
    @pytest.mark.parametrize(  # type: ignore[misc]
        "max_attempts,expected_attempts",
        [
            (3, 3),
            (5, 5),
            (1, 1),
        ],
    )
    async def test_command_retry_pattern(
        self,
        command_bus: CommandBus,
        test_command_class: type[Command],
        max_attempts: int,
        expected_attempts: int,
    ) -> None:
        """Test retry pattern with parametrized attempts"""
        attempt_count = 0

        class RetryHandler(CommandHandler[dict[str, Any]]):
            async def handle(self, command: Command) -> CommandResult[dict[str, Any]]:
                nonlocal attempt_count
                attempt_count += 1

                if attempt_count < max_attempts:
                    return CommandResult.failure(f"Attempt {attempt_count} failed")

                return CommandResult.success({"attempts": attempt_count})

            def can_handle(self, command: Command) -> bool:
                return True

        command_bus.register_handler(test_command_class, RetryHandler())
        command = test_command_class()

        result: CommandResult[dict[str, Any]] | None = None
        for _ in range(max_attempts):
            result = await command_bus.execute(command)
            if result.status == CommandResultStatus.SUCCESS:
                break

        assert result is not None
        assert result.status == CommandResultStatus.SUCCESS
        assert result.data is not None
        assert result.data["attempts"] == expected_attempts

    @pytest.mark.asyncio  # type: ignore[misc]
    @pytest.mark.parametrize("command_count", [1, 3, 5, 10])  # type: ignore[misc]
    async def test_command_chain_execution(
        self,
        command_bus: CommandBus,
        command_factory: CommandFactory,
        command_count: int,
    ) -> None:
        """Test chain of command executions with various chain lengths"""
        execution_log: list[str] = []

        class LoggingHandler(CommandHandler[dict[str, Any]]):
            def __init__(self, name: str) -> None:
                self.name = name

            async def handle(self, command: Command) -> CommandResult[dict[str, Any]]:
                execution_log.append(f"{self.name}:{command.get_command_type()}")
                return CommandResult.success({"handler": self.name})

            def can_handle(self, command: Command) -> bool:
                return True

        commands = [
            command_factory.create_command(step=i) for i in range(command_count)
        ]

        for i, command in enumerate(commands):
            handler = LoggingHandler(f"handler_{i}")
            command_bus.register_handler(type(command), handler)

            result = await command_bus.execute(command)
            assert result.status == CommandResultStatus.SUCCESS

        assert len(execution_log) == command_count
        for i, log_entry in enumerate(execution_log):
            assert log_entry.startswith(f"handler_{i}:")
