from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_kb() -> InlineKeyboardMarkup:
    """Клавиатура главного меню."""
    builder = InlineKeyboardBuilder()
    builder.button(text="💰 Купить голду", callback_data="menu:gold")
    builder.button(text="⭐ Купить подписку", callback_data="menu:subscription")
    builder.button(text="🚀 Буст аккаунта", callback_data="menu:boost")
    builder.button(text="🛠 Поддержка", callback_data="menu:support")
    builder.adjust(1)
    return builder.as_markup()


def payment_kb(item_key: str) -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой оплаты и возвратом в меню."""
    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Оплатить", callback_data=f"pay:{item_key}")
    builder.button(text="⬅️ Назад в меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def back_kb() -> InlineKeyboardMarkup:
    """Клавиатура только с кнопкой возврата."""
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад в меню", callback_data="menu:main")
    builder.adjust(1)
    return builder.as_markup()


def support_kb(privacy_url: str, terms_url: str) -> InlineKeyboardMarkup:
    """
    Клавиатура раздела поддержки:
    - "Политика конфиденциальности" и "Пользовательское соглашение" в одну строку
    - "Назад в меню" отдельной строкой снизу
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="🔒 Политика конфиденциальности", url=privacy_url)
    builder.button(text="📄 Пользовательское соглашение", url=terms_url)
    builder.button(text="⬅️ Назад в меню", callback_data="menu:main")
    builder.adjust(2, 1)
    return builder.as_markup()
