from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

import keyboards as kb
from content import BOOST, GOLD, MAIN_MENU, PAYMENT_STUB, SUBSCRIPTION, SUPPORT
from utils import send_section

router = Router()

SECTIONS = {
    "gold": GOLD,
    "subscription": SUBSCRIPTION,
    "boost": BOOST,
}


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Команда /start — показываем главное меню."""
    await send_section(message, MAIN_MENU, "main", reply_markup=kb.main_menu_kb())


@router.callback_query(F.data == "menu:main")
async def cb_main_menu(callback: CallbackQuery) -> None:
    """Кнопка "Назад в меню"."""
    await send_section(callback, MAIN_MENU, "main", reply_markup=kb.main_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "menu:support")
async def cb_support(callback: CallbackQuery) -> None:
    """Кнопка "Поддержка"."""
    await send_section(callback, SUPPORT, "support", reply_markup=kb.back_kb())
    await callback.answer()


@router.callback_query(F.data.startswith("menu:"))
async def cb_section(callback: CallbackQuery) -> None:
    """Кнопки "Купить голду" / "Купить подписку" / "Буст аккаунта"."""
    key = callback.data.split(":", 1)[1]
    section = SECTIONS.get(key)
    if section is None:
        await callback.answer()
        return
    await send_section(callback, section, key)
    await callback.answer()


@router.callback_query(F.data.startswith("pay:"))
async def cb_pay(callback: CallbackQuery) -> None:
    """
    Кнопка "Оплатить" — пока заглушка.
    Здесь в будущем нужно подключить реальную платёжную систему
    (например, ЮKassa, CryptoBot, Telegram Payments и т.д.)
    """
    await callback.answer(PAYMENT_STUB["alert"], show_alert=True)
