from datetime import UTC, datetime
from typing import Any


class SentNotification:
    """Record of a sent notification"""

    def __init__(
        self,
        recipient: str,
        message: str,
        sent_at: datetime,
        metadata: dict[str, Any] | None = None,
    ):
        self.recipient = recipient
        self.message = message
        self.sent_at = sent_at
        self.metadata = metadata or {}


class FakeTelegramNotificationService:
    """
    Fake Telegram notification service

    Implements same interface as TelegramNotificationService
    but stores messages in memory instead of sending them.
    """

    def __init__(self, bot_token: str = "fake_token"):
        """Initialize fake service"""
        self.bot_token = bot_token
        self._sent_notifications: list[SentNotification] = []

    def send(
        self, recipient: str, message: str, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Fake send - stores notification instead of sending

        Args:
            recipient: Telegram chat ID
            message: Message text
            metadata: Optional metadata

        Returns:
            Success response mimicking Telegram API
        """
        notification = SentNotification(
            recipient=recipient,
            message=message,
            sent_at=datetime.now(UTC),
            metadata=metadata,
        )

        self._sent_notifications.append(notification)

        return {"ok": True, "message_id": len(self._sent_notifications)}

    def get_sent_notifications(self) -> list[SentNotification]:
        """Get all sent notifications"""
        return self._sent_notifications.copy()

    def get_notifications_to(self, recipient: str) -> list[SentNotification]:
        """Get notifications sent to specific recipient"""
        return [
            notif for notif in self._sent_notifications if notif.recipient == recipient
        ]

    def count_sent(self) -> int:
        """Count total sent notifications"""
        return len(self._sent_notifications)

    def clear(self):
        """Clear all sent notifications"""
        self._sent_notifications.clear()

    def was_sent_to(self, recipient: str, message_contains: str) -> bool:
        """Check if message containing text was sent to recipient"""
        for notif in self._sent_notifications:
            if notif.recipient == recipient and message_contains in notif.message:
                return True
        return False

    def last_message_to(self, recipient: str) -> str | None:
        """Get last message sent to recipient"""
        messages = self.get_notifications_to(recipient)
        if messages:
            return messages[-1].message
        return None
