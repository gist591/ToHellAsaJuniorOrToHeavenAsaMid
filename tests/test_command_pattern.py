import pytest

from to_the_hell.oncallhub.domain.commands import (
    Command,
    CommandBus,
    CommandHandler,
    CommandResult,
    CommandResultStatus,
)


def test_command_result_success():
    """Test successful command result creation"""
    data = {"id": 1, "name": "test"}
    result = CommandResult.success(data)

    assert result.status == CommandResultStatus.SUCCESS
    assert result.data == data
    assert result.error_message is None
    assert result.validation_errors is None


def test_command_result_failure():
    """Test failure command result creation"""
    error_msg = "Something went wrong"
    result = CommandResult.failure(error_msg)

    assert result.status == CommandResultStatus.FAILURE
    assert result.data is None
    assert result.error_message == error_msg
    assert result.validation_errors is None


def test_command_result_validation_error():
    """Test validation error command result creation"""
    validation_errors = {"title": ["Title is required"], "email": ["Invalid email"]}
    result = CommandResult.validation_error(validation_errors)

    assert result.status == CommandResultStatus.VALIDATION_ERROR
    assert result.data is None
    assert result.error_message is None
    assert result.validation_errors == validation_errors


def test_command_result_status_values():
    """Test command result status enum values"""
    assert CommandResultStatus.SUCCESS.value == "success"
    assert CommandResultStatus.FAILURE.value == "failure"
    assert CommandResultStatus.VALIDATION_ERROR.value == "validation_error"


def test_command_interface():
    """Test that Command is an abstract base class"""
    with pytest.raises(TypeError):
        Command()


def test_command_handler_interface():
    """Test that CommandHandler is an abstract base class"""
    with pytest.raises(TypeError):
        CommandHandler()


def test_command_bus_initialization():
    """Test command bus initialization"""
    bus = CommandBus()
    assert bus._handlers == {}


def test_command_bus_register_handler():
    """Test registering handler with command bus"""
    bus = CommandBus()

    class TestCommand(Command):
        def get_command_type(self) -> str:
            return "test_command"

    class TestHandler(CommandHandler[dict]):
        async def handle(self, command: Command) -> CommandResult[dict]:
            return CommandResult.success({"test": "data"})

        def can_handle(self, command: Command) -> bool:
            return isinstance(command, TestCommand)

    handler = TestHandler()
    bus.register_handler(TestCommand, handler)

    assert bus._handlers[TestCommand] == handler


@pytest.mark.asyncio
async def test_command_bus_execute():
    """Test executing command through command bus"""
    bus = CommandBus()

    class TestCommand(Command):
        def get_command_type(self) -> str:
            return "test_command"

    class TestHandler(CommandHandler[dict]):
        async def handle(self, command: Command) -> CommandResult[dict]:
            return CommandResult.success({"test": "data"})

        def can_handle(self, command: Command) -> bool:
            return isinstance(command, TestCommand)

    handler = TestHandler()
    bus.register_handler(TestCommand, handler)

    command = TestCommand()
    result = await bus.execute(command)

    assert result.status == CommandResultStatus.SUCCESS
    assert result.data == {"test": "data"}


@pytest.mark.asyncio
async def test_command_bus_execute_handler_not_found():
    """Test error when handler not found"""
    bus = CommandBus()

    class TestCommand(Command):
        def get_command_type(self) -> str:
            return "test_command"

    command = TestCommand()

    with pytest.raises(ValueError, match="Handler for command TestCommand not found"):
        await bus.execute(command)
