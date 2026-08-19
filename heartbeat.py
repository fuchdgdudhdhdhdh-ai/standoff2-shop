"""
"Автобудилка" — каждые N минут (по умолчанию 10) бот отправляет сообщение
в указанный канал/чат о том, что он активен и работает.
"""

import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config

logger = logging.getLogger(__name__)


async def _send_heartbeat(bot: Bot) -> None:
    if not config.HEARTBEAT_CHANNEL_ID:
        logger.warning("HEARTBEAT_CHANNEL_ID не задан — автопинг пропущен")
        return
    try:
        await bot.send_message(
            chat_id=config.HEARTBEAT_CHANNEL_ID,
            text="✅ Бот активен и работает исправно.",
        )
        logger.info("Heartbeat отправлен")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Не удалось отправить heartbeat: %s", exc)


def setup_heartbeat(bot: Bot) -> AsyncIOScheduler:
    """Создаёт и настраивает планировщик, но не запускает его (start() вызывается отдельно)."""
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(
        _send_heartbeat,
        trigger="interval",
        minutes=config.HEARTBEAT_INTERVAL_MINUTES,
        args=[bot],
        id="heartbeat",
        replace_existing=True,
    )
    return scheduler
