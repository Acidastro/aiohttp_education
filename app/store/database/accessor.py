# Аксессор — сущность, которая помогает работать с данными,
# находящимися вне памяти приложения, например, бывает аксессор к базе данных или аксессор к стороннему API.

from aiohttp import web

from app.forum.models import Message
from app.store.database.models import db


class PostgresAccessor:
    """Отвечает за подключение к базе данных и отключение после завершения работы"""

    def __init__(self) -> None:
        self.message = Message
        self.db = None

    def setup(self, application: web.Application) -> None:
        """
        Использует сигналы aiohttp. Добавляя в списки (startup,cleanup),
        вызывает функции при включении и выключении приложения.
        """
        application.on_startup.append(self._on_connect)  # включит бд
        application.on_cleanup.append(self._on_disconnect)  # отключит бд

    async def _on_connect(self, application: web.Application):
        """Берет данные о базе из конфигурационного файла """
        self.config = application["config"]["postgres"]
        await db.set_bind(self.config["database_url"])  # создает необходимое подключение к базе
        self.db = db

    async def _on_disconnect(self, _) -> None:
        """Позволяет отключиться от базы после завершения работы приложения и освободить ресурсы базы"""
        if self.db is not None:
            await self.db.pop_bind().close()
