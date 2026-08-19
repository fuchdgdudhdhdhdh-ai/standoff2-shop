"""
Общая логика отправки "разделов" меню (фото + текст + кнопки).
Перед отправкой нового сообщения удаляется предыдущее сообщение бота в этом чате.
"""

from typing import Union

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

# Простое хранилище "последнее сообщение бота" в памяти: {chat_id: message_id}
# Для одного инстанса бота на Render этого достаточно.
_last_bot_message: dict[int, int] = {}


async def _delete_previous(bot, chat_id: int) -> None:
    msg_id = _last_bot_message.get(chat_id)
    if msg_id is None:
        return
    try:
        await bot.delete_message(chat_id=chat_id, message_id=msg_id)
    except TelegramBadRequest:
        # Сообщение уже удалено пользователем/слишком старое — просто игнорируем
        pass


async def send_section(
    event: Union[Message, CallbackQuery],
    section: dict,
    section_key: str,
    reply_markup: InlineKeyboardMarkup | None = None,
) -> None:
    """
    Универсальная отправка раздела меню.
    Работает и из обычного сообщения (команда), и из CallbackQuery (нажатие кнопки).
    """
    import keyboards as kb

    if isinstance(event, CallbackQuery):
        chat_id = event.message.chat.id
        bot = event.bot
    else:
        chat_id = event.chat.id
        bot = event.bot

    await _delete_previous(bot, chat_id)

    markup = reply_markup if reply_markup is not None else kb.payment_kb(section_key)

    sent = await bot.send_photo(
        chat_id=chat_id,
        photo=section["photo"],
        caption=section["text"],
        reply_markup=markup,
    )
    _last_bot_message[chat_id] = sent.message_id
