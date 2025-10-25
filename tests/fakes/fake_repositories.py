from datetime import datetime


class FakeDuty:
    """In-memory duty model"""

    def __init__(
        self,
        id: int,
        devops_id: int,
        start_time: datetime,
        end_time: datetime,
        reminder_24h_sent: bool = False,
        reminder_2h_sent: bool = False,
        reminder_10m_sent: bool = False,
    ):
        self.id = id
        self.devops_id = devops_id
        self.start_time = start_time
        self.end_time = end_time
        self.reminder_24h_sent = reminder_24h_sent
        self.reminder_2h_sent = reminder_2h_sent
        self.reminder_10m_sent = reminder_10m_sent


class FakeUser:
    """In-memory user model"""

    def __init__(
        self, id: int, email: str, full_name: str, telegram_chat_id: str | None = None
    ):
        self.id = id
        self.email = email
        self.full_name = full_name
        self.telegram_chat_id = telegram_chat_id


class FakeDutyRepository:
    """
    In-memory duty repository for testing

    Stores duties in a list and provides same interface as real repository
    """

    def __init__(self):
        """Initialize with empty storage"""
        self._duties: list[FakeDuty] = []

    def add(self, duty: FakeDuty) -> FakeDuty:
        """
        Add duty to storage

        Args:
            duty: Duty to add

        Returns:
            Added duty
        """
        self._duties.append(duty)
        return duty

    def get_by_id(self, duty_id: int) -> FakeDuty | None:
        """
        Get duty by ID

        Args:
            duty_id: Duty identifier

        Returns:
            Duty if found, None otherwise
        """
        for duty in self._duties:
            if duty.id == duty_id:
                return duty
        return None

    def find_starting_between(
        self, start: datetime, end: datetime, reminder_field: str
    ) -> list[FakeDuty]:
        """
        Find duties starting in time window that haven't received specific reminder

        Args:
            start: Window start time
            end: Window end time
            reminder_field: Field name to check (e.g., 'reminder_24h_sent')

        Returns:
            List of duties matching criteria
        """
        result = []
        for duty in self._duties:
            if (start <= duty.start_time <= end) and (
                not getattr(duty, reminder_field)
            ):
                result.append(duty)
        return result

    def update(self, duty: FakeDuty) -> FakeDuty:
        """
        Update duty in storage

        Args:
            duty: Duty with updated fields

        Returns:
            Updated duty
        """
        # In-memory update is automatic (mutable object)
        # Just return the duty
        return duty

    def clear(self):
        """Clear all duties (for test cleanup)"""
        self._duties.clear()

    def count(self) -> int:
        """Get total number of duties"""
        return len(self._duties)


class FakeUserRepository:
    """
    In-memory user repository for testing
    """

    def __init__(self):
        """Initialize with empty storage"""
        self._users: list[FakeUser] = []

    def add(self, user: FakeUser) -> FakeUser:
        """
        Add user to storage

        Args:
            user: User to add

        Returns:
            Added user
        """
        self._users.append(user)
        return user

    def get_by_id(self, user_id: int) -> FakeUser | None:
        """
        Get user by ID

        Args:
            user_id: User identifier

        Returns:
            User if found, None otherwise
        """
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def clear(self):
        """Clear all users (for test cleanup)"""
        self._users.clear()

    def count(self) -> int:
        """Get total number of users"""
        return len(self._users)
