"""
Конфигурация бота.
Все значения берутся из переменных окружения (.env локально, Environment Variables на Render).
Ничего в этом файле редактировать не нужно — настройки задаются через .env / панель Render.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота, выданный @BotFather
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

# Telegram ID администратора (для будущих админ-команд)
ADMIN_ID: int = int(os.getenv("ADMIN_ID", "0") or "0")

# ID канала/чата, куда бот будет слать "я живой" каждые N минут.
# Формат: -1001234567890 (узнать можно через @getidsbot или @username_to_id_bot)
HEARTBEAT_CHANNEL_ID: str = os.getenv("HEARTBEAT_CHANNEL_ID", "")

# Интервал автопинга в минутах
HEARTBEAT_INTERVAL_MINUTES: int = int(os.getenv("HEARTBEAT_INTERVAL_MINUTES", "10"))

# Юзернейм поддержки, подставляется в раздел "Поддержка"
SUPPORT_USERNAME: str = os.getenv("SUPPORT_USERNAME", "@your_support")

# Порт для веб-сервера (Render сам передаёт переменную PORT)
PORT: int = int(os.getenv("PORT", "10000"))
