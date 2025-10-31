# OnCall Hub

Система для управления дежурствами в DevOps команде. Назначаешь дежурных, следишь за инцидентами, получаешь напоминания в телеграм.

## Что умеет

- Расписание дежурств с проверкой пересечений
- Инциденты с lifecycle (создал -> назначил -> в работе -> решил -> закрыл)
- Телеграм напоминания за 24ч/2ч/10мин до начала дежурства
- JWT авторизация с refresh токенами
- Фоновые задачи через Celery

## Стек

Python 3.13, FastAPI, PostgreSQL, SQLAlchemy 2.0 async, Redis, Celery, Docker

## Запуск

Через Docker (проще всего):
```bash
git clone <repo>
cd oncallhub
docker-compose up -d
```

API будет на localhost:8000, swagger на /docs

Локально нужен Python 3.13+, PostgreSQL и Redis:
```bash
pip install uv
uv sync

# создай .env с настройками БД и Redis

uv run alembic upgrade head
uv run uvicorn to_the_hell.oncallhub.api.main:app --reload

# в другом терминале celery worker
uv run celery -A to_the_hell.oncallhub.workers.celery_app worker
```

## Структура

```
to_the_hell/oncallhub/
├── api/              # роутеры, схемы, зависимости
├── domain/           # сущности, команды, бизнес-логика
│   ├── entities/
│   ├── commands/
│   └── application/handlers/
├── infra/db/         # ORM модели, репозитории
└── workers/          # celery задачи
```

Архитектура по Clean Architecture - слои разделены, зависимости идут только вниз. Domain не знает про FastAPI или PostgreSQL.

Паттерны: Command для операций, Repository для данных, State для инцидентов, Value Objects для типобезопасности.

## Примеры API

Логин:
```bash
curl -X POST http://localhost:8000/auth/login \
  -d '{"username": "john", "password": "secret"}'
```

Создать дежурство:
```bash
curl -X POST http://localhost:8000/duties/put-on-duty \
  -H "Authorization: Bearer <token>" \
  -d '{"devops_id": 1, "start_time": "2025-10-31T09:00:00Z", "end_time": "2025-10-31T17:00:00Z"}'
```

## Разработка

Качество кода:
```bash
uv run ruff format .
uv run ruff check . --fix
uv run mypy to_the_hell/
```

Тесты:
```bash
uv run pytest
uv run pytest --cov
```

Миграции:
```bash
uv run alembic revision --autogenerate -m "описание"
uv run alembic upgrade head
```

## Добавление новой фичи

Базовый флоу:

1. Команда в `domain/commands/`
2. Обработчик в `domain/application/handlers/`
3. Регистрация в CommandBus
4. Роутер в `api/routers/`
5. Тесты

Пример в коде:
```python
# команда
@dataclass
class UpdateDutyCommand(Command):
    duty_id: int
    status: bool

# обработчик
class UpdateDutyHandler:
    async def handle(self, command):
        duty = await self.repo.get_by_id(command.duty_id)
        duty.status = command.status
        await self.repo.update(duty)
        return CommandResult.success(duty)

# роутер
@router.patch("/duties/{id}")
async def update(id: int, data: Schema, bus: CommandBusDep):
    result = await bus.execute(UpdateDutyCommand(id, data.status))
    return result.data
```

## Deployment

Docker Compose для простых случаев, Kubernetes для скейлинга.

Базовый `docker-compose.prod.yml`:
```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${DATABASE_USER}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
  
  redis:
    image: redis:7-alpine
  
  app:
    image: oncallhub:latest
    ports: ["8000:8000"]
    depends_on: [db, redis]
  
  worker:
    image: oncallhub:latest
    command: celery -A ... worker
```

Для прода добавь nginx с SSL и rate limiting.

## Частые вопросы

**Зачем Command Pattern?**
Чтобы контроллеры не раздувались. Вся логика в обработчиках, контроллеры только переводят HTTP в команды.

**Entity vs Value Object?**
Entity если есть ID и меняется (Duty, Incident). Value Object если неизменяемый и определяется атрибутами (TimeRange).

**Где валидация?**
Pydantic проверяет HTTP данные, обработчики команд - бизнес-правила, Value Objects - инварианты.

## Roadmap

- Email/SMS уведомления
- Правила эскалации
- Интеграция с календарями
- Slack бот
- Dashboard с метриками

## Лицензия

CC BY-NC-SA 4.0

Подробнее: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
