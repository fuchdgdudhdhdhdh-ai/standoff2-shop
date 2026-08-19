import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web

import config
from handlers import commands, menu
from heartbeat import setup_heartbeat

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def health(_request: web.Request) -> web.Response:
    """Health-check эндпоинт — нужен, чтобы Render видел, что сервис жив."""
    return web.Response(text="Standoff2 Shop Bot is alive ✅")


async def start_web_server() -> None:
    """
    Render (как и большинство хостингов для Web Service) требует, чтобы
    приложение слушало $PORT. Поднимаем лёгкий aiohttp-сервер параллельно с ботом.
    """
    app = web.Application()
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", config.PORT)
    await site.start()
    logger.info("Веб-сервер запущен на порту %s", config.PORT)


async def main() -> None:
    if not config.BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN не задан. Добавьте его в .env (локально) "
            "или в Environment Variables на Render."
        )

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(menu.router)
    dp.include_router(commands.router)

    scheduler = setup_heartbeat(bot)
    scheduler.start()

    await start_web_server()

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен, начинаю polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
