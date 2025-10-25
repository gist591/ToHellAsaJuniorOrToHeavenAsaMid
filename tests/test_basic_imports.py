from typing import Any


def test_basic_imports() -> None:
    """Test basic imports"""
    from to_the_hell.oncallhub.domain.commands import (
        Command,
        CommandBus,
        CommandHandler,
        CommandResult,
        CommandResultStatus,
    )

    assert Command is not None
    assert CommandHandler is not None
    assert CommandResult is not None
    assert CommandResultStatus is not None
    assert CommandBus is not None


def test_incident_priority_import() -> None:
    """Test incident priority imports"""
    from to_the_hell.oncallhub.domain.value_objects.incident_priority import (
        IncidentPriority,
    )

    assert IncidentPriority.LOW == IncidentPriority.LOW
    assert IncidentPriority.HIGH == IncidentPriority.HIGH
    assert IncidentPriority.CRITICAL > IncidentPriority.LOW


def test_command_result_creation() -> None:
    """Test command result creation"""
    from to_the_hell.oncallhub.domain.commands import CommandResult, CommandResultStatus

    success_result: CommandResult[dict[str, Any]] = CommandResult.success(
        {"id": 1, "name": "test"}
    )
    assert success_result.status == CommandResultStatus.SUCCESS
    assert success_result.data == {"id": 1, "name": "test"}

    failure_result: CommandResult[str] = CommandResult.failure("Something went wrong")
    assert failure_result.status == CommandResultStatus.FAILURE
    assert failure_result.error_message == "Something went wrong"

    validation_errors = {"title": ["Title is required"]}
    validation_result: CommandResult[Any] = CommandResult.validation_error(
        validation_errors
    )
    assert validation_result.status == CommandResultStatus.VALIDATION_ERROR
    assert validation_result.validation_errors == validation_errors
