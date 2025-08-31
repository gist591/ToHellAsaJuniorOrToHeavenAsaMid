class NotificationStrategy(ABC):
    """Abstract strategy for notification"""

    @abstractmethod
    async def send_notification(
        self, message: str, recipients: List[str], **kwargs
    ) -> bool:
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        pass
