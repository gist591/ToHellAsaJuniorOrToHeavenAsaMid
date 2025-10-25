from dataclasses import dataclass


@dataclass
class Devops:
    """
    DevOps user domain entity
    """

    id: int
    name: str
    telegram_chat_id: str
    email: str
    phone: str
