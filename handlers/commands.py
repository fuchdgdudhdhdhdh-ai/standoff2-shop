from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import keyboards as kb
from content import BOOST, GOLD, SUBSCRIPTION, SUPPORT
from utils import send_section

router = Router()


@router.message(Command("gold"))
async def cmd_gold(message: Message) -> None:
    """Команда /gold — сразу открывает раздел покупки голды."""
    await send_section(message, GOLD, "gold")


@router.message(Command("subscription"))
async def cmd_subscription(message: Message) -> None:
    """Команда /subscription — сразу открывает раздел покупки подписки."""
    await send_section(message, SUBSCRIPTION, "subscription")


@router.message(Command("boost"))
async def cmd_boost(message: Message) -> None:
    """Команда /boost — сразу открывает раздел буста аккаунта."""
    await send_section(message, BOOST, "boost")


@router.message(Command("support"))
async def cmd_support(message: Message) -> None:
    """Команда /support — сразу открывает раздел поддержки."""
    await send_section(message, SUPPORT, "support", reply_markup=kb.back_kb())
