from uuid import UUID

from to_the_hell.oncallhub.domain.utils.properties_from_models import make_property


class User:
    id = make_property('id')
    name = make_property('name')
    telegram_username = make_property('telegram_username')

    def __init__(self, id: UUID, name: str, telegram_username: str = ''):
        self._id = id
        self._name = name
        self._telegram_username = telegram_username
