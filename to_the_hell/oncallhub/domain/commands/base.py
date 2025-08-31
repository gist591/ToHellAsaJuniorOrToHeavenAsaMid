from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

T = TypeVar("T")


class CommandResultStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    VALIDATION_ERROR = "validation_error"


@dataclass
class CommandResult(Generic[T]):
    status: CommandResultStatus
    data: T | None = None
    error_message: str | None = None
    validation_errors: dict[str, list[str]] | None = None

    @classmethod
    def success(cls, data: T) -> "CommandResult[T]":
        return cls(status=CommandResultStatus.SUCCESS, data=data)

    @classmethod
    def failure(cls, error_message: str) -> "CommandResult[T]":
        return cls(status=CommandResultStatus.FAILURE, error_message=error_message)

    @classmethod
    def validation_error(
        cls, validation_errors: dict[str, list[str]]
    ) -> "CommandResult[T]":
        return cls(
            status=CommandResultStatus.VALIDATION_ERROR,
            validation_errors=validation_errors,
        )


class Command(ABC):
    @abstractmethod
    def get_command_type(self) -> str:
        """Return command type identifier"""
        pass


class CommandHandler(ABC, Generic[T]):
    @abstractmethod
    async def handle(self, command: Command) -> CommandResult[T]:
        pass

    @abstractmethod
    def can_handle(self, command: Command) -> bool:
        pass


class CommandBus:
    def __init__(self) -> None:
        self._handlers: dict[type, CommandHandler] = {}

    def register_handler(self, command_type: type, handler: CommandHandler) -> None:
        self._handlers[command_type] = handler

    async def execute(self, command: Command) -> CommandResult:
        command_type = type(command)

        if command_type not in self._handlers:
            raise ValueError(f"Handler for command {command_type.__name__} not found")

        handler = self._handlers[command_type]
        return await handler.handle(command)
