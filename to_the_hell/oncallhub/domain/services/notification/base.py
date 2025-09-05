from abc import ABC, abstractmethod
from typing import Any


class NotificationStrategy(ABC):
    """Abstract strategy for notification"""

    @abstractmethod
    async def send_notification(
        self, message: str, recipients: list[str], **kwargs: Any
    ) -> bool:
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        pass
